# Generator.py

from langchain.embeddings import HuggingFaceEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains import ConversationalRetrievalChain
from pinecone import Pinecone

class generator:
    def __init__(self, pinecone_api_key, groq_api_key, pinecone_index_name):
        self.pc = Pinecone(api_key=pinecone_api_key)
        self.index = self.pc.Index(pinecone_index_name)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.pinecone_vector_store = PineconeVectorStore(index=self.index, embedding=self.embeddings)
        self.llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

        self.prompt_template = PromptTemplate(
            template="""
            Given the following doctors' notes on a patient consultation:  
            "{summaries}"  
            
            Based on relevant medical documents, define the patient's case, suggest the medical process, and provide detailed guidance on preparing the treatment environment for receiving the patient from the ambulance.  
            
            Your response should include:  
            - **Diagnosis or potential medical condition.**  
            - **Steps for further medical investigation.**  
            - **Required equipment, medications, and staff preparation.**  
            - **Specific protocols for receiving the patient from the ambulance, including:**  
            - **Immediate stabilization procedures.**  
            - **Preparation of the emergency treatment area (e.g., ICU, trauma room).**  
            - **Coordination with paramedics for seamless handover.**  
            - **Emergency response team roles and readiness.**  
            - **Infection control or isolation measures if necessary.**  
            
            Use the retrieved documents to support the response.
            """,
            input_variables=["summaries"],
        )

        self.question_generator = LLMChain(llm=self.llm, prompt=CONDENSE_QUESTION_PROMPT, verbose=False)
        self.doc_chain = load_qa_with_sources_chain(self.llm, chain_type="stuff", verbose=False, prompt=self.prompt_template)
        self.qa_chain = ConversationalRetrievalChain(
            retriever=self.pinecone_vector_store.as_retriever(),
            question_generator=self.question_generator,
            combine_docs_chain=self.doc_chain,
            verbose=False,
        )

    def process_medical_summary(self, conversation_summary):
        response = self.qa_chain.invoke({
            "question": self.prompt_template.format(summaries=conversation_summary),
            "chat_history": [],
        })
        return response.get("answer", "")
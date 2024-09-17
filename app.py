import streamlit as st
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.retrievers import BM25Retriever, EnsembleRetriever

import os

# Set your Hugging Face API token
HUGGINGFACEHUB_API_TOKEN = ''

# Initialize embeddings
@st.cache_resource
def get_embeddings():
    return HuggingFaceInferenceAPIEmbeddings(
        api_key=HUGGINGFACEHUB_API_TOKEN,
        model_name="sentence-transformers/all-MiniLM-l6-v2"
    )

# Load and process documents
@st.cache_resource
def load_documents():
    loader = TextLoader("Data/report.txt", encoding='utf-8')
    report = loader.load()
    loader = TextLoader("Data/statistics.txt", encoding='utf-8')
    statistics = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(report)
    return chunks + statistics

# Create vector database
@st.cache_resource
def create_vector_db(_docs, _embeddings):
    return Chroma.from_documents(documents=_docs, embedding=_embeddings, collection_metadata={"dimension": 384})

# Initialize retrievers
@st.cache_resource
def init_retrievers(_vector_db, _chunks):
    vectorstore_retriever = _vector_db.as_retriever(search_kwargs={"k": 3})
    keyword_retriever = BM25Retriever.from_documents(_chunks)
    keyword_retriever.k = 3
    return EnsembleRetriever(
        retrievers=[vectorstore_retriever, keyword_retriever],
        weights=[0.5, 0.5]
    )

# Initialize LLM
@st.cache_resource
def init_llm():
    return HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        model_kwargs={"temperature": 0.3, "max_new_tokens": 1024},
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    )

# Set up the chain
def setup_chain(retriever, llm):
    template = """
    <|system|>>
    You are a helpful AI Assistant that follows instructions extremely well.
    Use the following context to answer user question.

    Think step by step before answering the question. 

    CONTEXT: {context}
    </s>
    <|user|>
    {query}
    </s>
    <|assistant|>
    """
    prompt = ChatPromptTemplate.from_template(template)
    output_parser = StrOutputParser()

    return (
        {"context": retriever, "query": RunnablePassthrough()}
        | prompt
        | llm
        | output_parser
    )

# Streamlit app
def main():
    st.title("RAG Application")

    # Initialize components
    embeddings = get_embeddings()
    docs = load_documents()
    vector_db = create_vector_db(docs, embeddings)
    retriever = init_retrievers(vector_db, docs)
    llm = init_llm()
    chain = setup_chain(retriever, llm)

    # User input
    query = st.text_input("Ask a question:")

    if query:
        with st.spinner("Generating answer..."):
            response = chain.invoke(query)
            st.write(response)

if __name__ == "__main__":
    main()
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import streamlit as st
import logging


def split_documents(documents):
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        return splitter.split_documents(documents)
    except Exception as e:
        logging.error(f"Error splitting documents: {str(e)}", exc_info=True)
        raise RuntimeError("Failed to build the search index.")


@st.cache_resource
def get_embeddings():
    try:
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    except Exception as e:
        logging.error(f"Error loading HuggingFaceEmbeddings model: {str(e)}", exc_info=True)
        raise RuntimeError("Failed to build the search index.")


def create_vector_store(chunks):
    try:
        embeddings = get_embeddings()
        vectorstore = FAISS.from_documents(
            chunks,
            embeddings
        )
        return vectorstore
    except Exception as e:
        logging.error(f"Error creating vector store index: {str(e)}", exc_info=True)
        raise RuntimeError("Failed to build the search index.")
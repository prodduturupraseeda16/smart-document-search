import streamlit as st
from utils.pdf_reader import load_pdf
from utils.vector_store import split_documents, create_vector_store
from utils.ai_helper import get_llm
import logging

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Smart Document Search",
    page_icon="📄",
    layout="wide"
)

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.title("📂 Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("⚙️ Process Documents"):

        if uploaded_files:
            try:
                with st.spinner("Reading PDF files..."):
                    all_documents = []
                    for file in uploaded_files:
                        docs = load_pdf(file)
                        all_documents.extend(docs)

                with st.spinner("Processing index..."):
                    chunks = split_documents(all_documents)
                    vectorstore = create_vector_store(chunks)

                st.session_state.vectorstore = vectorstore
                st.session_state.chunks = chunks

                st.success("✅ Documents processed successfully!")
                st.write(f"📄 Total Pages : {len(all_documents)}")
                st.write(f"🧩 Total Chunks : {len(chunks)}")
                st.success("🚀 AI is ready to answer questions!")
            except Exception as e:
                logging.error(f"Failed to process documents: {str(e)}", exc_info=True)
                if "Failed to build the search index" in str(e):
                    st.error("❌ Failed to build the search index.")
                else:
                    st.error("❌ Unable to process the uploaded PDF.")
        else:
            st.warning("Please upload at least one PDF.")

    # -------------------------------
    # SUMMARY FEATURE
    # -------------------------------
    st.subheader("📝 Document Summary")

    if st.button("Generate Summary"):

        if "chunks" in st.session_state:
            try:
                with st.spinner("Generating summary..."):
                    llm = get_llm()

                    text = "\n\n".join(
                        [c.page_content for c in st.session_state.chunks[:5]]
                    )

                    prompt = f"""
                    Summarize the following document in simple bullet points:

                    {text}
                    """

                    response = llm.invoke(prompt)

                    st.write(response.content)
            except Exception as e:
                logging.error(f"Summarization error: {str(e)}", exc_info=True)
                st.error("❌ The AI service is temporarily unavailable. Please try again later.")
        else:
            st.warning("Please process a PDF first.")

    # -------------------------------
    # CLEAR CHAT BUTTON (NEW)
    # -------------------------------
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.success("Chat cleared!")
        st.rerun()

    st.markdown("---")
    st.info("Upload PDF → Process → Ask Questions")

# -------------------------------
# MAIN PAGE
# -------------------------------
st.title("📄 Smart Document Search System")

st.markdown("Chat with your PDF documents using AI 🤖")

# -------------------------------
# CHAT UI & HISTORY
# -------------------------------
st.subheader("💬 Chat with PDF")

# Display chat messages from history on app rerun
for role, msg in st.session_state.chat_history:
    if role == "You":
        with st.chat_message("user"):
            st.write(msg)
    else:
        with st.chat_message("assistant"):
            st.write(msg)

# React to new user input
if question := st.chat_input("Ask something from your document:"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.write(question)

    if st.session_state.vectorstore is not None:
        try:
            with st.spinner("AI is thinking..."):
                try:
                    docs = st.session_state.vectorstore.similarity_search(question, k=3)
                except Exception as search_err:
                    logging.error(f"Search retrieval error: {str(search_err)}", exc_info=True)
                    st.error("❌ Failed to query the search index.")
                    st.stop()

                try:
                    llm = get_llm()
                    context = "\n\n".join([d.page_content for d in docs])

                    prompt = f"""
                    Answer based only on the context below.

                    Context:
                    {context}

                    Question:
                    {question}
                    """

                    response = llm.invoke(prompt)
                    answer = response.content
                except Exception as llm_err:
                    logging.error(f"LLM API query error: {str(llm_err)}", exc_info=True)
                    st.error("❌ The AI service is temporarily unavailable. Please try again later.")
                    st.stop()

            # Display AI response inside assistant chat bubble
            with st.chat_message("assistant"):
                st.write(answer)
                st.markdown("### 📌 Sources")
                for idx, doc in enumerate(docs):
                    page_num = doc.metadata.get("page", None)
                    page_label = f"Page {page_num + 1}" if page_num is not None else "Page N/A"

                    if idx > 0:
                        st.markdown("---")
                    st.markdown(f"📍 **{page_label}**")
                    st.info(doc.page_content[:300])

            # Save to session chat history
            st.session_state.chat_history.append(("You", question))
            st.session_state.chat_history.append(("AI", answer))
        except Exception as e:
            logging.error(f"Unexpected chat query error: {str(e)}", exc_info=True)
            st.error("❌ An unexpected error occurred. Please try again.")
    else:
        st.warning("Please upload and process a PDF first.")
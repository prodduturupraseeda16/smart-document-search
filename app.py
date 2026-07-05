import streamlit as st
from utils.pdf_reader import load_pdf
from utils.vector_store import split_documents, create_vector_store
from utils.ai_helper import get_llm

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

            with st.spinner("Reading PDF files..."):

                all_documents = []

                for file in uploaded_files:
                    docs = load_pdf(file)
                    all_documents.extend(docs)

            chunks = split_documents(all_documents)

            vectorstore = create_vector_store(chunks)

            st.session_state.vectorstore = vectorstore
            st.session_state.chunks = chunks

            st.success("✅ Documents processed successfully!")
            st.write(f"📄 Total Pages : {len(all_documents)}")
            st.write(f"🧩 Total Chunks : {len(chunks)}")
            st.success("🚀 AI is ready to answer questions!")

        else:
            st.warning("Please upload at least one PDF.")

    # -------------------------------
    # SUMMARY FEATURE
    # -------------------------------
    st.subheader("📝 Document Summary")

    if st.button("Generate Summary"):

        if "chunks" in st.session_state:

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
# CHAT UI
# -------------------------------
st.subheader("💬 Chat with PDF")

question = st.text_input("Ask something from your document:")

if st.button("Send"):

    if question:

        if st.session_state.vectorstore is not None:

            llm = get_llm()

            docs = st.session_state.vectorstore.similarity_search(question, k=3)

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

            # Save chat history
            st.session_state.chat_history.append(("You", question))
            st.session_state.chat_history.append(("AI", answer))

            st.markdown("### 🤖 Answer")
            st.write(answer)

            # Sources
            st.markdown("### 📌 Sources")
            for i, doc in enumerate(docs):
                st.info(doc.page_content[:300])

        else:
            st.warning("Please upload and process a PDF first.")

    else:
        st.warning("Please enter a question.")

# -------------------------------
# CHAT HISTORY DISPLAY (CHATGPT STYLE)
# -------------------------------
st.markdown("---")
st.subheader("🧾 Chat History")

for role, msg in st.session_state.chat_history:
    if role == "You":
        with st.chat_message("user"):
            st.write(msg)
    else:
        with st.chat_message("assistant"):
            st.write(msg)
import time
import requests
import streamlit as st


# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise RAG Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }

    .status-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .source-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 0.75rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 Enterprise RAG Knowledge Assistant")

st.caption(
    "Upload documents, build a searchable knowledge base, "
    "and ask questions using retrieval-augmented generation."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.header("System")

    try:
        health_response = requests.get(
            f"{API_URL}/health",
            timeout=5,
        )

        if health_response.status_code == 200:
            st.success("FastAPI: Online")
        else:
            st.error("FastAPI: Error")

    except requests.RequestException:
        st.error("FastAPI: Offline")

    st.divider()

    st.subheader("Retrieval Pipeline")

    st.write("📄 Document Loader")
    st.write("✂️ Text Chunking")
    st.write("🧠 Hugging Face Embeddings")
    st.write("🔎 FAISS Vector Search")
    st.write("🎯 Re-ranking")
    st.write("✨ Groq LLM")


# --------------------------------------------------
# Document Upload
# --------------------------------------------------

st.header("📚 Knowledge Base")

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "docx", "txt", "md"],
    help="Supported formats: PDF, DOCX, TXT, MD",
)


# --------------------------------------------------
# Background indexing
# --------------------------------------------------

if uploaded_file is not None:

    if st.button("🚀 Upload & Index Document", type="primary"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        }

        try:
            with st.spinner("Uploading document..."):

                response = requests.post(
                    f"{API_URL}/documents",
                    files=files,
                    timeout=60,
                )

            if response.status_code != 200:
                st.error(
                    f"Upload failed: {response.text}"
                )
            else:

                result = response.json()

                job_id = result["job_id"]

                st.session_state["job_id"] = job_id
                st.session_state["indexed_file"] = uploaded_file.name

                st.success(
                    "Document uploaded. Background indexing started."
                )

        except requests.RequestException as exc:
            st.error(
                f"Unable to connect to FastAPI backend: {exc}"
            )


# --------------------------------------------------
# Monitor indexing job
# --------------------------------------------------

if "job_id" in st.session_state:

    job_id = st.session_state["job_id"]

    st.subheader("⚙️ Indexing Status")

    status_placeholder = st.empty()
    progress_bar = st.progress(0)

    while True:

        try:

            response = requests.get(
                f"{API_URL}/documents/status/{job_id}",
                timeout=10,
            )

            if response.status_code != 200:
                st.error(
                    f"Unable to check indexing status: "
                    f"{response.text}"
                )
                break

            job = response.json()

            status = job.get("status")
            stage = job.get("stage")
            chunks = job.get("chunks", 0)
            error = job.get("error")

            if status == "queued":

                status_placeholder.info(
                    "⏳ Waiting for indexing worker..."
                )

                progress_bar.progress(10)

            elif status == "processing":

                if "Extracting" in stage:

                    status_placeholder.info(
                        "📄 Extracting and chunking document..."
                    )

                    progress_bar.progress(30)

                elif "FAISS" in stage:

                    status_placeholder.info(
                        f"🧠 Building FAISS index... "
                        f"{chunks:,} chunks"
                    )

                    progress_bar.progress(75)

                else:

                    status_placeholder.info(stage)

                    progress_bar.progress(50)

            elif status == "completed":

                progress_bar.progress(100)

                status_placeholder.success(
                    f"✅ Document indexed successfully — "
                    f"{chunks:,} chunks"
                )

                st.session_state["index_ready"] = True

                break

            elif status == "failed":

                progress_bar.empty()

                status_placeholder.error(
                    "❌ Document indexing failed."
                )

                if error:
                    st.error(error)

                st.session_state["index_ready"] = False

                break

            time.sleep(2)

        except requests.RequestException as exc:

            status_placeholder.error(
                f"Unable to connect to FastAPI backend: {exc}"
            )

            break


# --------------------------------------------------
# Question Answering
# --------------------------------------------------

if st.session_state.get("index_ready", False):

    st.divider()

    st.header("💬 Ask Your Documents")

    question = st.text_input(
        "Enter your question",
        placeholder="Ask something about the uploaded document...",
    )

    if st.button("🔍 Ask Question", type="primary"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                with st.spinner(
                    "Searching documents and generating answer..."
                ):

                    response = requests.post(
                        f"{API_URL}/ask",
                        json={
                            "question": question
                        },
                        timeout=120,
                    )

                if response.status_code != 200:

                    st.error(
                        f"Question failed: {response.text}"
                    )

                else:

                    result = response.json()

                    st.subheader("Answer")

                    st.write(
                        result.get(
                            "answer",
                            "No answer generated.",
                        )
                    )

                    sources = result.get(
                        "sources",
                        [],
                    )

                    if sources:

                        st.subheader(
                            "📚 Retrieved Sources"
                        )

                        for index, source in enumerate(
                            sources,
                            start=1,
                        ):

                            with st.expander(
                                f"Source {index} — "
                                f"{source.get('source', 'Unknown')}"
                            ):

                                st.write(
                                    f"**Page:** "
                                    f"{source.get('page', 'N/A')}"
                                )

                                st.write(
                                    f"**Relevance Score:** "
                                    f"{source.get('score', 'N/A')}"
                                )

                                st.write(
                                    source.get(
                                        "content",
                                        "",
                                    )
                                )

            except requests.RequestException as exc:

                st.error(
                    f"Unable to connect to FastAPI backend: {exc}"
                )

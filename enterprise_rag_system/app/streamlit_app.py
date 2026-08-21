import streamlit as st
import requests

st.set_page_config(page_title="Enterprise RAG", page_icon="📚", layout="wide")
st.title("Enterprise RAG Knowledge Assistant")
st.caption("Upload documents, build a searchable knowledge base, and ask grounded questions.")

api_url = st.sidebar.text_input("API URL", "http://localhost:8000")

uploaded = st.file_uploader("Upload a document", type=["pdf", "docx", "txt", "md"])
if uploaded and st.button("Index document"):
    response = requests.post(
        f"{api_url}/documents",
        files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
        timeout=180,
    )
    if response.ok:
        st.success(f"Indexed {response.json()['chunks_indexed']} chunks.")
    else:
        st.error(response.text)

question = st.chat_input("Ask a question about your documents")
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        try:
            response = requests.post(
                f"{api_url}/ask", json={"question": question}, timeout=180
            )
            if response.ok:
                result = response.json()
                st.write(result["answer"])
                with st.expander("Sources"):
                    for src in result["sources"]:
                        st.write(src)
            else:
                st.error(response.text)
        except requests.RequestException as exc:
            st.error(f"API connection failed: {exc}")

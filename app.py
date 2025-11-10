import streamlit as st
from dotenv import load_dotenv

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with your docs", layout="wide", page_icon="📄")

    st.header("📄 Chat with your docs!")
    st.text_input("Ask a question about your documents:")
    with st.sidebar:
        # st.header("Upload your documents")
        # uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
        # if uploaded_files:
        #     st.success(f"Uploaded {len(uploaded_files)} files successfully!")

        st.subheader("Upload your documents")
        uploaded_files = st.file_uploader("Choose PDF files and click on Process", type="pdf", accept_multiple_files=True)
        st.button("Process")
        if uploaded_files:
            st.success(f"Uploaded {len(uploaded_files)} files successfully!")

if __name__ == "__main__":      
    main()
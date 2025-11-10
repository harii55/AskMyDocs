import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter

def get_pdf_text(uploaded_files):
    text = ""
    for pdf_file in uploaded_files:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


# def get_text_chunks(text, chunk_size=500, overlap=50):
#     text_chunks = []
#     start = 0
#     text_length = len(text)
#     while start < text_length:
#         end = min(start + chunk_size, text_length)
#         text_chunks.append(text[start:end])
#         start += chunk_size - overlap
#     return text_chunks


def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks


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
        if uploaded_files:
            st.success(f"Uploaded {len(uploaded_files)} files successfully!")
        
        if st.button("Process"):
            with st.spinner("Processing files..."):

                #get pdf text
                raw_text = get_pdf_text(uploaded_files)
                # st.write(raw_text) 

                #get the text chunks
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)


                #create the vector store


    
            



if __name__ == "__main__":      
    main()
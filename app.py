import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInstructEmbeddings, HuggingFaceEmbeddings

from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationalRetrievalChain

from htmlTemplate import css, bot_template, user_template

#NOTE: langchain has removed memory and chains from main package, and is using some other technics..
#langchain_classic is used to access older version of langchain, it contains deprecated modules like memory and chains




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

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vectorstore(text_chunks):

    # method 1: using openai
    # embeddings = OpenAIEmbeddings()

    # method 2: using huggingface
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    llm = ChatOpenAI(
        openai_api_base="https://ai.megallm.io/v1",
        openai_api_key=os.getenv("OPENAI_API_KEY"),  # Or os.getenv("MEGALLM_API_KEY") if renamed
        model="gpt-5-mini",  # Use MegaLLM's model
        temperature=0
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)  #keep full transcript as memory
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain
    
def handle_user_question(user_question):
    answer = st.session_state.conversation({"question": user_question})
    st.write(answer)  #complete object with 'answer' and 'chat_history' keys!


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with your docs", layout="wide", page_icon="📄")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None #initialize variable in session state if not present


    st.header("📄 Chat with your docs!")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_user_question(user_question)

    st.write(user_template.replace("{{MSG}}", user_question), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Bot's response goes here"), unsafe_allow_html=True)
  
    
    
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
                # st.write(text_chunks)


                #create the vector store
                vector_store = get_vectorstore(text_chunks)
                # st.write(vector_store)

                # create conversation chain
                conversation = get_conversation_chain(vector_store)
                st.session_state.conversation = conversation  #store this variable in session state so that when streamlit reloads, this variable is not lost 
                st.success("Processing completed!")           #also this is used when we want to use this var outside of the scope of this if block (here sidebar)

                


    
            



if __name__ == "__main__":      
    main()
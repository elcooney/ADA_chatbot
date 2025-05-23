
# don't forget to work in: 
# virtual environment based on "requirements.txt"

############################################################
# import all dependencies


import os
import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain.callbacks import get_openai_callback

## new dependencies based on new structure, code via writesonic: 
from PIL import Image
import pytesseract
import pandas as pd
from langchain_community.document_loaders import UnstructuredExcelLoader

############################################################
# set the API key


os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

############################################################
# set folder path(s) for PDFs


folder_path = "resources"

############################################################
# define functions


## 1. clear history when opening in new browser

def clear_history():
    if 'crc' in st.session_state:
        del st.session_state['crc']

## 2. load PDF documents from specified folder on my computer

# old code below, kept as reference:
'''@st.cache_resource
def load_and_process_pdfs():
    try:
        documents = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                file_path = os.path.join(folder_path, filename)
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())

        if not documents:
            st.error(f"No PDF files found in {folder_path}")
            return None

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        vector_store = Chroma.from_documents(chunks, embedding=embeddings, persist_directory='db')

        llm = ChatOpenAI(model='gpt-4', temperature=0.7)
        retriever = vector_store.as_retriever(search_kwargs={"k":3})
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"  # Specify the output key for memory storage
        )

        crc = ConversationalRetrievalChain.from_llm(
            llm,
            retriever,
            memory=memory,
            return_source_documents=True,
            output_key="answer"  # Specify the output key for the chain
        )
        return crc
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
'''

## new code via writesonic: 
@st.cache_resource
def load_and_process_documents():
    try:
        documents = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if filename.lower().endswith('.pdf'):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
            
            elif filename.lower().endswith('.png'):
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                documents.append(Document(page_content=text, metadata={"source": filename}))
            
            elif filename.lower().endswith(('.xlsx', '.xls')):
                loader = UnstructuredExcelLoader(file_path)
                documents.extend(loader.load())

        if not documents:
            st.error(f"No supported files found in {folder_path}")
            return None

        # Rest of the function remains the same as original code
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        vector_store = Chroma.from_documents(chunks, embedding=embeddings, persist_directory='db')

        llm = ChatOpenAI(model='gpt-4', temperature=0.7)
        retriever = vector_store.as_retriever(search_kwargs={"k":3})
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        crc = ConversationalRetrievalChain.from_llm(
            llm,
            retriever,
            memory=memory,
            return_source_documents=True,
            output_key="answer"
        )
        return crc
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

############################################################
# Begin Code


# create UI with streamlit
st.title('Chat with ArchitectBot about ADA Requirements')

# Load and process PDFs
if 'crc' not in st.session_state:
    st.session_state.crc = load_and_process_documents() #adjusted to include new function name
    st.success("Documents processed and embedded successfully.") #adjusted to address 'Documents' rather than just 'PDFs'

# Create a form for the question input and submit button
with st.form(key='question_form'):
    question = st.text_input('Input your question')
    submit_button = st.form_submit_button(label='Submit Question')

# generate response to question
if submit_button and question:

    # confirming PDfs have been processed and embedded successfully
    if 'crc' in st.session_state:
        crc = st.session_state.crc

        # retreive response to question from conversation retreival chain
        with get_openai_callback() as cb:
            result = crc({'question': question})
            response = result['answer']
            source_documents = result['source_documents']

        # print response to user
        st.write("Chatbot: " + response)

        # # display citations
        # st.subheader("Citations")
        # for i, doc in enumerate(source_documents):
        #     st.write(f"{i+1}. {doc.metadata['source']}, Page {doc.metadata['page']}")

# ############################################################
        # Display chat history (uncomment if needed)
        st.subheader("Chat History")
        messages = crc.memory.chat_memory.messages
        for message in messages:
            if message.type == 'human':
                st.write("Human: " + message.content)
            elif message.type == 'ai':
                st.write("AI: " + message.content)

        # # Display token usage (uncomment if needed)
        # st.subheader("Token Usage")
        # st.write(f"Total Tokens: {cb.total_tokens}")
        # st.write(f"Prompt Tokens: {cb.prompt_tokens}")
        # st.write(f"Completion Tokens: {cb.completion_tokens}")
        # st.write(f"Total Cost (USD): ${cb.total_cost:.4f}")
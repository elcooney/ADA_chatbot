# Additional imports for loading PDF documents and QA chain.
from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain

from transformers import pipeline

import gradio as gr

# Specify the folder path
folder_path = "embedded_resources/"

# Get all files in the folder and add them to a list
file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Print the list of files
print(len(file_list))

def ada_chatbot(query):
    # pdf_loader = PyPDFLoader('embedded_resources\CHAPTER_3_BUILDING_BLOCKS_307.pdf') 
    # documents = pdf_loader.load()

    for file in file_list:
        if os.path.exists(file):
            pdf_loader = PyPDFLoader(file)
            document = pdf_loader.load()
            file_list.extend(document)
        else:
            print(f"Warning: file not found - {file}")
            pass


    llm = ChatGoogleGenerativeAI(google_api_key=GEMINI_API_KEY, model=GEMINI_MODEL, temperature=0.0)

    chain = load_qa_chain(llm)

    result = chain.invoke({"input_documents": file_list, "question": query})
    return result["output_text"]

# Create an instance of the Gradio Interface application function with parameters. 
app = gr.Interface(fn=ada_chatbot, 
                   title="American Disabilities Act Chatbot",
                   description="Ask the chatbot about the ADA requirements per '2021 Accessibility Pocketbook 2021 IBC®, 2021 IEBC® and ICC A117.1-2017'.",
                   inputs=["text"], 
                   outputs=gr.Textbox(lines=20, label="Summarized Response", show_copy_button=True))
# Launch the app
app.launch()

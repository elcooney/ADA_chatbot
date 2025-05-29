# ArchitectBot: ADA Requirements Chatbot

A user-friendly chatbot application that allows architects, builders, and the general public to ask questions about ADA (Americans with Disabilities Act) requirements and receive accurate, relevant answers based on official documentation.

![ArchitectBot Screenshot](https://via.placeholder.com/800x450.png?text=ArchitectBot+Screenshot)

## 🌟 Features

- **Intuitive Chat Interface**: Simply type your question about ADA requirements and receive an immediate response
- **Smart Document Processing**: Automatically processes and understands:
  - PDF documents
  - Images (using OCR technology)
  - Excel spreadsheets
- **Conversation Memory**: Remembers previous questions and answers for contextual conversations
- **Citation Support**: Can provide sources for its answers from the loaded documents
- **Built with Streamlit**: Clean, responsive web interface that works on desktop and mobile

## 📋 Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system (for image processing)
- OpenAI API key

## 🔧 Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/architectbot.git
   cd architectbot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   - Create a `.streamlit/secrets.toml` file in the project directory
   - Add your API key to the file:
     ```
     OPENAI_API_KEY = "your-api-key-here"
     ```

5. Add your ADA documentation:
   - Create a `resources` folder in the project directory
   - Place PDF files, images, and Excel spreadsheets containing ADA requirements in this folder

## 🚀 Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in your terminal (typically http://localhost:8501)

3. Type your question about ADA requirements in the text input field and click "Submit Question"

4. View the chatbot's response and any relevant citations

## 🧠 How It Works

1. **Document Processing**: The application loads documents from the `resources` folder, processes them using various techniques (PDF parsing, OCR for images, etc.), and splits them into smaller chunks.

2. **Embedding Creation**: Each chunk is converted into a vector embedding using OpenAI's embedding model.

3. **Vector Database**: These embeddings are stored in a Chroma vector database for efficient retrieval.

4. **Question Processing**: When you ask a question, the application:
   - Converts your question into an embedding
   - Finds the most similar document chunks in the vector database
   - Sends these relevant chunks and your question to GPT-4
   - Returns a comprehensive answer based on the ADA documentation

5. **Conversation Memory**: The system maintains a history of your conversation, allowing for follow-up questions and contextual understanding.

## 🔍 Technologies Used

- **Streamlit**: For the web interface
- **LangChain**: For document processing and conversation chains
- **OpenAI GPT-4**: For generating high-quality, contextual responses
- **Chroma DB**: For vector storage and similarity search
- **PyTesseract**: For OCR (Optical Character Recognition) on images
- **Pandas**: For handling Excel data

## ⚠️ Limitations

- Requires an OpenAI API key (usage will incur costs)
- Answer quality depends on the comprehensiveness of the loaded ADA documents
- Large document collections may require significant processing time on first run

## 🔮 Future Improvements

- Support for more document types (Word, HTML, etc.)
- Enhanced citation capabilities with direct page references
- Document upload through the UI
- Performance optimizations for faster processing

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgements

- OpenAI for providing the GPT models
- The Streamlit team for their amazing framework
- LangChain for their document processing capabilities

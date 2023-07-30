import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationChain

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Use the API key in your code
os.environ["OPENAI_API_KEY"] = api_key

# location of the pdf file.
documents = PdfReader("chatgpt-backend/data/MAP_DATA.pdf")

# read data from the file then put it into a variable called raw_text
raw_text = ""
for i, page in enumerate(documents.pages):
    text = page.extract_text()
    if text:
        raw_text += text

# We need to split the text that we read into smaller chunks so that
# during information retreival we don't hit the token size limits.
text_splitter = CharacterTextSplitter(
    separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len,
)
texts = text_splitter.split_text(raw_text)

# Create an instance of OpenAIEmbeddings for embeddings
embeddings = OpenAIEmbeddings()

docsearch = FAISS.from_texts(texts, embeddings)

chain = load_qa_chain(OpenAI(), chain_type="stuff")

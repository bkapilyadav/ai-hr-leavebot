from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Load and embed the policy
loader = PyPDFLoader("leave_policy.pdf")
docs = loader.load()

vectordb = Chroma.from_documents(docs, embedding=OpenAIEmbeddings(), persist_directory="policy_db")
vectordb.persist()

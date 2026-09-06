# rag_engine.py

import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

def load_documents(data_folder="."):
    loader = DirectoryLoader(data_folder, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()
    if not docs:
        raise FileNotFoundError(
            f"No .txt files found in '{data_folder}/'. "
            f"Make sure your data files are in that folder before running this script."
        )
    return docs

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=40)
    return splitter.split_documents(documents)

def build_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return FAISS.from_documents(chunks, embeddings)

_retriever = None
_llm = None

def initialize(data_folder="."):
    global _retriever, _llm
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY environment variable is not set. "
            "Get a free key at https://console.groq.com and set it before running."
        )
    docs = load_documents(data_folder)
    chunks = split_documents(docs)
    vectorstore = build_vectorstore(chunks)
    _retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    _llm = ChatGroq(groq_api_key=api_key, model_name="openai/gpt-oss-20b", temperature=0)
    print(f"Initialized: loaded {len(docs)} files, split into {len(chunks)} chunks.")

def get_answer(question):
    if _retriever is None or _llm is None:
        initialize()

    docs = _retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)

    full_prompt = (
        "You are a helpful enquiry assistant for K J Somaiya Institute of "
               "Technology (KJSIT). Use the context below to answer the question "
        "completely — when the context lists multiple related items "
        "(such as subjects, labs, projects, or documents), include every "
        "one of them, not just a partial selection. When stating any fee, total, or "
        "numeric figure, only report numbers that are explicitly written "
        "in the context — do not calculate, sum, or derive any number "
        "yourself, even if it seems like simple addition. Respond in the "
        "same language the question was asked in. If the context truly "
        "has nothing relevant to the question, say: \"I don't have that "
        "information. Please contact the college office at "
        "info.tech@somaiya.edu for accurate details.\"\n\n"
        "When listing subjects for a semester, always list the core subjects first, then a separate 'Labs:' line, then a separate 'Additional components:' line."
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )

    try:
        response = _llm.invoke(full_prompt)
        return response.content
    except Exception as e:
        return f"Sorry, something went wrong answering that question. ({e})"

def debug_retrieval(question):
    if _retriever is None:
        initialize()
    docs = _retriever.invoke(question)
    print(f"\n--- Retrieved {len(docs)} chunks ---")
    for i, d in enumerate(docs):
        print(f"\n[{i+1}] {d.page_content}")
    print("--- end ---\n")

if __name__ == "__main__":
    print("Initializing KJSIT Enquiry Bot... (this may take a minute the first time)")
    initialize()
    print("\nReady! Type a question, or 'quit' to exit.\n")
    while True:
        q = input("Ask a question: ")
        if q.strip().lower() == "quit":
            break
        print("\n" + get_answer(q) + "\n")
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# --- Load environment variables ---
load_dotenv(".env")
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("Missing GROQ_API_KEY. Please add it to your .env file.")

# --- LangChain Imports ---
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import chromadb
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# --- Load PDF & Prepare Data ---
def setup_rag_pipeline():
    # Load file
    loader = PyPDFLoader("Constitution.pdf")
    data = loader.load()

    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    text_chunks = text_splitter.split_documents(data)

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Setup Chroma
    client = chromadb.PersistentClient(path="my_chroma_db")
    collection = client.get_or_create_collection(name="pdf_collection")

    if collection.count() == 0:
        collection.add(
            documents=[d.page_content for d in text_chunks],
            metadatas=[d.metadata for d in text_chunks],
            embeddings=embeddings.embed_documents([d.page_content for d in text_chunks]),
            ids=[str(i) for i in range(len(text_chunks))]
        )

    vectordb = Chroma(
        client=client,
        collection_name="pdf_collection",
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 10}
    )

    # LLM
    llm = ChatGroq(
        temperature=0.2,
        groq_api_key=groq_api_key,
        model_name="llama-3.3-70b-versatile"
    )

    # Prompt
    system_prompt = (
        "You are a highly respected Senior Advocate of Pakistan specializing in constitutional law. "
        "Use the retrieved legal context (from the Constitution, Acts, and case law) to answer the user's question. "
        "If unsure, say 'Sorry I don't know about this based on the given sources'. "
        "You are made and trained by Khizar Ishtiaq."
        "Keep all valid answers professional, precise, and within 1–2 sentences unless more detail is absolutely required."
        "Keep answers professional, very precise only give answer that fulfill the requirements avoid lengthy answers be precise and concise. "
        "Cite the relevant Article or Section if possible.\n\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    return rag_chain

# Initialize RAG pipeline once
rag_chain = setup_rag_pipeline()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        query = data.get('question', '').strip()
        
        if not query:
            return jsonify({'error': 'Please enter a question'}), 400
        
        response = rag_chain.invoke({"input": query})
        answer = response.get("answer", "No relevant section found.")
        
        return jsonify({'answer': answer})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
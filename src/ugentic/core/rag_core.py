# Core implementation for Retrieval-Augmented Generation (RAG)

from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader # Added for document loading
import json
import os
import nltk
from datetime import datetime

# Initialize NLTK (for advanced text processing if needed)
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download("punkt")


ENABLE_RAG = True  # Toggle for Retrieval-Augmented Generation
SAVE_HISTORY = True

def get_embedding_model_from_config(filesystem_tool):
    """Reads the embedding model name from the config file."""
    # Navigate three levels up from core -> ugentic -> src -> project root
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.json')
    try:
        response = filesystem_tool.read_file(config_path)
        if response["status"] == "success":
            config = json.loads(response["content"])
            return config.get("embedding_model", "embeddinggemma:latest")  # Better default
        else:
            return "embeddinggemma:latest"
    except Exception:
        return "embeddinggemma:latest"

# This will be initialized in the main application
EMBEDDING_MODEL = None

def get_ollama_embeddings(embedding_model=None):
    """Initializes and returns the Ollama embeddings model."""
    model_name = embedding_model or EMBEDDING_MODEL or "embeddinggemma:latest"
    return OllamaEmbeddings(model=model_name)

def get_text_splitter(chunk_size=1000, chunk_overlap=200):
    """Creates and returns a text splitter for document chunking."""
    return RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

class RAGCore:
    def __init__(self, embedding_model, text_splitter, filesystem_tool):
        self.embeddings = embedding_model
        self.text_splitter = text_splitter
        self.filesystem_tool = filesystem_tool
        self.vector_store = {}
        print("RAG Core Initialized.")

    def add_document(self, doc_id, doc_content):
        """Processes and adds a document to the vector store."""
        chunks = self.text_splitter.split_text(doc_content)
        doc_vectors = self.embeddings.embed_documents(chunks)
        
        self.vector_store[doc_id] = {
            "chunks": chunks,
            "vectors": doc_vectors,
            "added_at": datetime.utcnow().isoformat()
        }
        print(f"Document '{doc_id}' added to vector store with {len(chunks)} chunks.")

    def load_documents_from_directory(self, directory_path, file_extensions=['.md', '.txt']):
        """Loads documents from a specified directory and adds them to the vector store."""
        # Use direct filesystem access for better reliability
        if not os.path.isdir(directory_path):
            print(f"Error: Directory not found at {directory_path}")
            return

        print(f"Loading documents from {directory_path}...")
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                if any(file_name.endswith(ext) for ext in file_extensions):
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        self.add_document(file_path, content)
                    except Exception as e:
                        print(f"Error loading {file_path}: {e}")
        print("Document loading complete.")

    def retrieve(self, query, top_k=3):
        """Retrieves the most relevant document chunks for a given query."""
        if not self.vector_store:
            print("Warning: RAG retrieval attempted on an empty vector store.")
            return []

        query_vector = self.embeddings.embed_query(query)
        similarities = []

        for doc_id, doc_data in self.vector_store.items():
            doc_vectors = doc_data["vectors"]
            chunks = doc_data["chunks"]
            
            for i, chunk_vector in enumerate(doc_vectors):
                # Calculate cosine similarity
                similarity = self._cosine_similarity(query_vector, chunk_vector)
                similarities.append({
                    "doc_id": doc_id,
                    "chunk_text": chunks[i],
                    "similarity": similarity
                })

        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]

    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        import numpy as np
        
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)

# Example Usage (for testing)
if __name__ == "__main__":
    from filesystem_tool import FilesystemTool
    
    # Create filesystem tool for testing
    filesystem_tool = FilesystemTool(
        server_command=["echo"], 
        allowed_paths=["C:\\Users\\craig\\Desktop\\MainProjects\\Ugentic_Dissertation"]
    )
    
    # Initialize components
    embedding_model_name = get_embedding_model_from_config(filesystem_tool)
    ollama_embed = get_ollama_embeddings(embedding_model_name)
    splitter = get_text_splitter()
    
    rag_system = RAGCore(ollama_embed, splitter, filesystem_tool)
    
    # Load documents from the Project_Tracker directory
    project_tracker_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Project_Tracker')
    rag_system.load_documents_from_directory(project_tracker_path)

    query = "What is the core vision of UGENTIC?"
    retrieved_chunks = rag_system.retrieve(query)
    
    print(f"\nQuery: {query}")
    print("Retrieved Chunks:")
    if retrieved_chunks:
        for chunk in retrieved_chunks:
            print(f"- (Similarity: {chunk['similarity']:.4f}) [Doc: {os.path.basename(chunk['doc_id'])}] {chunk['chunk_text']}")
    else:
        print("No relevant chunks retrieved.")

    query_hr = "How many vacation days are employees entitled to?"
    retrieved_hr_chunks = rag_system.retrieve(query_hr)

    print(f"\nQuery: {query_hr}")
    print("Retrieved HR Chunks:")
    if retrieved_hr_chunks:
        for chunk in retrieved_hr_chunks:
            print(f"- (Similarity: {chunk['similarity']:.4f}) [Doc: {os.path.basename(chunk['doc_id'])}] {chunk['chunk_text']}")
    else:
        print("No relevant chunks retrieved.")

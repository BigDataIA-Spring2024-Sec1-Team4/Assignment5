from pinecone import Pinecone, PodSpec
import os
from sentence_transformers import SentenceTransformer
import openai
import re

# Initialize Pinecone
api_key = "4f628185-246c-4089-a1a3-fce3aab8a307"
pinecone = Pinecone(api_key=api_key)

spec = PodSpec(environment="gcp-starter")

index_name = "combined-index"  # A single combined index for both questions and justifications

vector_dimension = 384
# index = pinecone.Index(name=index_name)

# if index in pinecone.list_indexes():
#     print(f"Index '{index_name}' already exists. Deleting it...")
#     if index.name == index_name:
#         pinecone.delete_index(name=index_name)

# Wait a few seconds for the index to be deleted before creating a new one
import time
time.sleep(5)
# Check if the combined index exists; if not, create it
if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, dimension=vector_dimension, metric="cosine", spec=spec)

# Connect to the index
combined_index = pinecone.Index(index_name)

def parse_and_vectorize(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    raw_entries = re.split(r'\n\d+\.', content)[1:]  # Split the content by numbers at the start of the entries
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    for entry_number, entry in enumerate(raw_entries, start=1):
        parts = entry.strip().split('\n\n')  # Split by double newlines
        
        # Ensure there are enough parts for a question and a justification
        if len(parts) < 4:
            print(f"Skipping entry {entry_number} due to missing data.")
            continue
        
        question_text = parts[0].strip()
        # Assuming the justification is always the last part
        justification_text = parts[-1].split(':', 1)[1].strip() if ':' in parts[-1] else "Justification missing"
        
        combined_vector = model.encode(f"{question_text} {justification_text}")
        
        combined_index.upsert(vectors=[(str(entry_number), combined_vector, {
            "question": question_text,
            "justification": justification_text
        })])

# Main flow
file_path = 'SetA_Questions.txt'  # Ensure this path is correct
parse_and_vectorize(file_path)

print("Vectorization and storage complete.")
# ---------------------
# # Define the index name
# index_name = "questions-answers-index"

# # Define the spec for the index
# # This is required as per the new Pinecone documentation
# spec = PodSpec(environment="gcp-starter")

# # Check if the index exists; if not, create it with the updated method
# if index_name not in pinecone.list_indexes():
#     pinecone.create_index(name=index_name, dimension=384, spec=spec)  # Assuming the embeddings are 768-dimensional

# # Connect to the index
# index = pinecone.Index(name=index_name)

# # Initialize the Sentence Transformer model for embeddings
# model = SentenceTransformer('all-MiniLM-L6-v2')

# # Example data
# questions = ["What is the capital of France?", "What is the largest planet in our solar system?"]
# answers = ["Paris", "Jupiter"]

# # Convert questions to embeddings
# question_embeddings = model.encode(questions)

# # Upsert embeddings into Pinecone index
# for i, q_emb in enumerate(question_embeddings):
#     index.upsert(vectors=[(str(i), q_emb, {"answer": answers[i]})])



# openai.api_key = os.getenv("OPENAI_API_KEY") or "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"

# # Embedding model to use from OpenAI
# EMBEDDING_MODEL = "text-embedding-ada-002"

# # Example query
# query = "What is the biggest planet?"

# # Generate embedding for the query
# embedded_query = openai.Embedding.create(input=query, model=EMBEDDING_MODEL)["data"][0]["embedding"]

# # Fetch top 1 most similar question's embedding and its metadata from Pinecone
# result = index.query(queries=[embedded_query], top_k=1)

# for match in result["matches"][0]:
#     print(f"Found match: {questions[int(match['id'])]}, Answer: {match['metadata']['answer']}")

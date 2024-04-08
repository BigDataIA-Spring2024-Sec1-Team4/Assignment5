import os
import re
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import openai

# Initialize Pinecone
api_key_pinecone = "4f628185-246c-4089-a1a3-fce3aab8a307"  # Replace with your actual Pinecone API key
pinecone = Pinecone(api_key=api_key_pinecone)

# Connect to the combined Pinecone index
combined_index = pinecone.Index("combined-index")

# Initialize the Sentence Transformer model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Set OpenAI API key
openai_api_key = "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"  # Replace with your actual OpenAI API key
openai.api_key = openai_api_key

def load_questions(file_path):
    """Load questions from a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = file.readlines()
    return [q.strip() for q in questions if q.strip()]

vector_dimension = 384
def retrieve_similar_questions_and_answers(query_question, top_k=3):
    """Retrieve top_k similar questions from Pinecone and their answers."""
    query_vector = model.encode([query_question])[0]
    # Ensure the vector dimension matches what's used in Pinecone
    query_vector_list = query_vector.tolist()[:vector_dimension]
    
    try:
        result = combined_index.query(queries=[query_vector_list], top_k=top_k)
        return [(match["metadata"]["question"], match["metadata"]["answer"]) for match in result["matches"][0]]
    except Exception as e:
        print(f"Error querying Pinecone: {str(e)}")
        return []

# Adjusted part for processing Set B questions
set_b_questions = load_questions('Set_B_Questions.txt')[:50]  # Safeguard to ensure no more than 50 questions are processed


def generate_gpt_prompt(question_b, similar_qa_pairs):
    """Generate a prompt for GPT based on the question from Set B and similar QA pairs."""
    prompt = f"Based on the following information, answer the question:\n\n"
    for i, (question, answer) in enumerate(similar_qa_pairs, start=1):
        prompt += f"Q{i}: {question}\nA{i}: {answer}\n\n"
    prompt += f"Question: {question_b}\nAnswer:"
    return prompt

def get_answer_with_gpt(question_b):
    """Get an answer for a question from Set B using similar QA pairs and GPT-3.5-turbo."""
    similar_qa_pairs = retrieve_similar_questions_and_answers(question_b)
    prompt = generate_gpt_prompt(question_b, similar_qa_pairs)
    response = openai.Completion.create(engine="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=150)
    return response.choices[0].text.strip()

# Load Set B questions
set_b_questions = load_questions('Set_B_Questions.txt')

# Process each question in Set B
for i, question_b in enumerate(set_b_questions, start=1):
    answer_with_justification = get_answer_with_gpt(question_b)
    print(f"Question {i}: {question_b}\nAnswer and Justification: {answer_with_justification}\n---\n")

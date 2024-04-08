import streamlit as st
import pandas as pd
import openai
import random

openai.api_key  = "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"

def get_sample_pattern():
    with open('sample_question_pattern.txt', 'r') as file:
        sample_question_pattern = file.read()
    return sample_question_pattern

def load_filtered_data(file_name, topics):
    df = pd.read_csv(file_name)
    filtered_df = df[df['topicName'].isin(topics)]
    return filtered_df

def generate_question(context, existing_questions):
    while True:
        prompt = f"Generate a unique multiple-choice question with 3 options and remember it considering all the topics from the context, the correct answer, and justification based on the following context:\n{context}\nEnsure that each generated question is distinct from the previous ones and that the questions are unique"
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",  # Adjust according to the model you're using
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        new_question = response.choices[0].text.strip()
        if new_question not in existing_questions:
            existing_questions.add(new_question)
            return new_question

def generate_questions_set(df, topics, num_questions):
    questions = set()
    while len(questions) < num_questions:
        random_topic = random.choice(topics)
        df_slice = df[df['topicName'] == random_topic].sample(n=1)
        question = generate_question(f"{df_slice['summary'].iloc[0]} {df_slice['learningOutcome'].iloc[0]}", questions)
        questions.add(question)
    return list(questions)

def save_questions_to_file(questions, filename):
    with open(filename, 'w') as file:
        for idx, question in enumerate(questions, start=1):
            file.write(f"{idx}. {question}\n\n")

# UI Setup
st.title('Question Bank Generator')

# Define tabs
tab_names = ["Set A", "Set B"]
tabs = st.tabs(tab_names)

# Load data
file_path = 'new_extracted_updated.csv'
topics = ["Market Efficiency", "Introduction to Industry and Company Analysis", "Equity Valuation: Concepts and Basic Tools"]
df = load_filtered_data(file_path, topics)

if not df.empty:
    # Process each tab
    for idx, tab in enumerate(tabs):
        st.write(f"## {tab_names[idx]} Questions")
        
        # Generate questions for the respective tab
        if st.button(f'Generate Questions {tab_names[idx]}'):
            questions_set = generate_questions_set(df, topics, 50)
            save_questions_to_file(questions_set, f'Set_{tab_names[idx]}_Questions.txt')
            
            # Display questions
            with open(f'Set_{tab_names[idx]}_Questions.txt', 'r') as file:
                st.code(file.read(), language='text')
                
            # Download button
            with open(f'Set_{tab_names[idx]}_Questions.txt', 'rb') as f:
                st.download_button(f'Download Set {tab_names[idx]} Questions', f, file_name=f'Set_{tab_names[idx]}_Questions.txt')
else:
    st.write("No data found for selected topics or file not found.")

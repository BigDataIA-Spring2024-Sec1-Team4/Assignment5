import streamlit as st
import csv
import re
import pandas as pd
import openai

# Set up your OpenAI API key

from openai import OpenAI
client = OpenAI(api_key = "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")

def generate_summary(learningOutcome,topic,summary):
    #prompt = f"Learning Outcome Statement: {los}\n\nTechnical Note:\n"
    prompt = f"A financial analyst with an MBA interested in learning more about the {topic}.\n\n generate a technical note that summarizes the key {learningOutcome} with given context as {summary}: \n\nTechnical Note:"
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()


def load_data(filepath):
    data = []
    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    #print("data:",data)
    return data

def filter_rows_by_topic(data, modified_topic):
    filtered_rows = []
    for row in data:
        if row['url'].endswith(modified_topic):
            filtered_rows.append(row) 
       
    return filtered_rows

def main():
    input_data = '../data/cleaned_extracted.csv'
    data = load_data(input_data)
    
    
    st.title("Select Topics")
    
    # Extract unique topic names
    topic_names = set(row["topicName"] for row in data)
    
    # Display all topic names
    selected_topics = st.multiselect("Select 3-4 topics:", list(topic_names))
    
    if len(selected_topics) < 3 or len(selected_topics) > 4:
        st.warning("Please select 3-4 topics.")
    else:
        selected_rows = []
        for row in data:
            if row["topicName"] in selected_topics:
                selected_rows.append(row)
        
        # Create DataFrame from selected rows
        df = pd.DataFrame(selected_rows, columns=["topicName", "introduction", "learningOutcome", "summary"])
        
        st.write("Selected Data:")
        st.write(df)

        # Generate summaries for Learning Outcome Statements
        st.write("Learning Outcome Summaries:")
        # for los in df["learningOutcome"]:
        #     summary = generate_summary(los)
        #     st.write(f"LOS: {los}")
        #     st.write(f"Summary: {summary}\n")
        for learningOutcome, topic_name, summary in zip(df["learningOutcome"], df["topicName"],df["summary"]):
            los = generate_summary(learningOutcome, topic_name, summary)
            st.write(f"Topic: {topic_name}")
            #st.write(f"Learning Outcome: {los}")
            st.write(f"Technical note: {los}\n")

if __name__ == "__main__":
    main()

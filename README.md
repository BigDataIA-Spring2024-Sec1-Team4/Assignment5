
## Assignment 5

## Problem Statement:
Development of a Structured Database and Text Extraction System for Finance Professional Development Resources

## Project Goals
Utilize Pinecone and OpenAI APIs to create knowledge summaries, generate a contextual knowledge base, utilize vector databases for question answering, and employ GPT-based summaries to provide accurate answers.

## Project Tasks
    
    ### Task 1: Creating Knowledge Summaries using OpenAI’s GPT
    
    **Goal:** To build a knowledge base from topic summaries and Learning Outcome Statements (LOS).  
    **Target User:** Financial analysts with an MBA seeking to understand LOS.  
    
    1. Generate technical notes summarizing key Learning Outcome Statements (LOS) using the provided context (summary, introduction, and LOS).
    2. Compile the notes into a markdown document.
    3. Chunk each LOS and its corresponding note and store it in Pinecone for efficient retrieval.
    
    ### Task 2: Generating a Knowledge Base (Q/A) providing context
    
    **Goal:** To develop a question/answer set for reinforcing learning from topic summaries.  
    **Target User:** Financial analysts with an MBA interested in LOS.  
    
    1. Create a question bank of 50 questions (Set A) with four options and one correct answer from the "Summary" section of each assigned topic.
    2. Parse sample documents for context and generate questions of similar complexity and type.
    3. Generate another set of 50 questions and answers (Set B) for comparison.
    4. Store Set A questions and answers separately in Pinecone.
    
    ### Task 3: Using a Vector Database to Find and Answer Questions
    
    **Goal:** To utilize a vector database to answer questions accurately.  
    **Target User:** Financial analysts with an MBA seeking efficient question answering.  
    
    1. Use RAG to search for similar questions and determine the accuracy of answers from Set B using information from Set A stored in Pinecone.
    2. Pass question-answer pairs from Set A to GPT-4 along with a question from Set B and answer choices.
    3. Evaluate the correctness of answers provided by GPT-4 and compare them to the actual answers.
    
    ### Task 4: Use Knowledge Summaries to Answer Questions
    
    **Goal:** To leverage knowledge summaries to answer questions effectively.  
    **Target User:** Financial analysts with an MBA aiming for accurate question answering.  
    
    1. Utilize RAG in the Pinecone vector database to find similar embeddings and LOS containing answers to questions from Set A and Set B.
    2. Tabulate the accuracy of answers to the 100 questions/topics.
    3. Discuss the effectiveness of this approach compared to Task 3 and propose alternative designs for improved question answering. 

## Conclusion

By completing these tasks, we aim to evaluate different approaches for knowledge retrieval and question answering using MaaS APIs, contributing valuable insights for enterprise applications.

## Codelab

[![codelabs](https://codelabs-preview.appspot.com/?file_id=1fgubqz6h9BDCbEH1wdWYCjpfK3Iof7RCu2W_Kd6uOAY#3)

[Demo]()

## Technologies Used

[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Snowflake](https://img.shields.io/badge/Snowflake-387BC3?style=for-the-badge&logo=snowflake&logoColor=light)](https://www.snowflake.com/)
[![Google Cloud Platform](https://img.shields.io/badge/Google%20Cloud%20Platform-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://www.streamlit.io/)
[![Pinecone](https://img.shields.io/badge/Pinecone-7B0099?style=for-the-badge&logo=pinecone&logoColor=white)](https://www.pinecone.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-000000?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)


## Project URLs


## Project Structure


## Architectural Diagram


## To run the application locally, follow these steps:



## Team Information and Contribution 

Name           | NUID          |
---------------|---------------|
Anirudh Joshi  | 002991365     |      
Nitant Jatale  | 002776669     |      
Rutuja More    | 00272782      |      

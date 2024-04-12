from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Python
from diagrams.programming.framework import FastAPI
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams import Node
from diagrams.custom import Custom
 
class OpenAI(Node):
    icon = "openai.png"
 
class Pinecone(Node):
    icon = "pinecone.png"
class Snowflake(Node):
    icon = "snowflake.png"
 
# Set 'outformat' to a higher resolution to increase the overall size of the diagram
with Diagram("System Architecture for Assignment5", show=False, direction="LR", outformat="png", graph_attr={"size": "25,25"}):
    with Cluster("Streamlit Frontend"):
        python_container = Docker("Streamlit Container")
        users = Custom("streamlit","./streamlit.png")
        python1 = Python("1: Process Learning Outcome")
        python2 = Python("2: Generate Question Bank")
        python3 = Python("3: Search Answers using Question Bank")
        python4 = Python("4: Generate Answers using Tech Notes")
        python_container >> users
        users >> python1
        users >> python2
        users >> python3
        users >> python4
 
    with Cluster("User Interaction"):
        users1 = Users("Questions")
        users2 = Users("Answers")
        python1 >> users1
        python2 >> users1
        python3 >> users2
        python4 >> users2
 
    with Cluster("FastAPI Services"):
        fastapi1 = FastAPI("Fast API Services")
        docker1 = Docker("FastApi Container")
        docker1 >> fastapi1
 
    with Cluster("External Services"):
        openai = Custom("OpenAI API","./openai.png")
        pinecone = Custom("Pinecone DB","./pinecone.png")
        snowflake = Custom("Snowflake DB","./snowflake.png")
 
    # Connect Python scripts to FastAPI services
    users1 >> fastapi1 >> snowflake
    snowflake >> openai >> pinecone
    users2 >> fastapi1 >> pinecone >> openai
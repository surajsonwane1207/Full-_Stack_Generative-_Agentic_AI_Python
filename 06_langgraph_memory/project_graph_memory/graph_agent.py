import os
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Neo4j credentials matching docker-compose
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "password"

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please create a .env file with your OpenAI API key.")
        return

    print("1. Connecting to Neo4j Graph Database...")
    try:
        graph = Neo4jGraph()
    except Exception as e:
        print(f"Failed to connect to Neo4j. Is the Docker container running? Error: {e}")
        return

    print("2. Initializing LLM and Graph Transformer...")
    # We use OpenAI here because graph extraction requires strong instruction following
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo-preview")
    llm_transformer = LLMGraphTransformer(llm=llm)

    print("3. Processing Sample Text...")
    text = """
    Alice is a software engineer who works at TechCorp.
    TechCorp is located in San Francisco.
    Alice is currently learning about LangGraph and Neo4j.
    Bob is Alice's manager at TechCorp.
    """
    
    documents = [Document(page_content=text)]
    
    print("4. Extracting Graph Documents (Nodes and Relationships)...")
    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    
    print(f"Extracted {len(graph_documents[0].nodes)} nodes and {len(graph_documents[0].relationships)} relationships.")
    
    for node in graph_documents[0].nodes:
        print(f"  Node: {node.id} ({node.type})")
    for rel in graph_documents[0].relationships:
        print(f"  Rel:  {rel.source.id} -[{rel.type}]-> {rel.target.id}")

    print("5. Saving to Neo4j...")
    graph.add_graph_documents(graph_documents)
    
    print("\nSuccess! You can now open the Neo4j Browser at http://localhost:7474")
    print("Log in with neo4j / password")
    print("Run the following Cypher query to see your graph: MATCH (n) RETURN n")

if __name__ == "__main__":
    main()

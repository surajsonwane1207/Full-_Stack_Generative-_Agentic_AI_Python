# Project: Graph Memory with Neo4j

This project demonstrates how to use LangChain and an LLM to automatically extract entities and relationships from raw text and construct a knowledge graph in Neo4j.

## What is Graph Memory?
Unlike Vector DBs that find semantically similar text, Graph DBs store explicit relationships (e.g., "Alice -[WORKS_AT]-> TechCorp"). This is crucial for agents that need episodic memory, complex reasoning, or multi-hop retrieval.

## Setup

1. Start the Neo4j database using Docker:
   ```bash
   docker-compose up -d
   ```

2. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your OpenAI API key (an LLM is needed to parse the text into a graph structure):
   ```env
   OPENAI_API_KEY=sk-your-key-here
   ```

## Usage

Run the agent script:
```bash
python graph_agent.py
```

1. The script will read a sample text about Alice.
2. It uses `LLMGraphTransformer` to parse the text into Nodes (Alice, TechCorp) and Relationships (WORKS_AT).
3. It pushes these to your local Neo4j container.

## Viewing your Graph
Open your browser and navigate to:
**http://localhost:7474**

- **Username**: neo4j
- **Password**: password

In the query bar at the top, run:
```cypher
MATCH (n) RETURN n
```
You will see a visual representation of the extracted knowledge graph!

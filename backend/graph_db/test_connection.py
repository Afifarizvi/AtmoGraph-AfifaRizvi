import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables from .env file
load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

def test_connection():
    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        driver.verify_connectivity()
        print("✅ Successfully connected to Neo4j AuraDB!")
    except Exception as e:
        print("❌ Connection failed:", e)
    finally:
        driver.close()

if __name__ == "__main__":
    test_connection()
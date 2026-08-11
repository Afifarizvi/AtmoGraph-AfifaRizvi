import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


class Neo4jClient:
    """Reusable Neo4j connection handler for AtmoGraph backend."""

    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    # ---- Helper methods ----

    def get_node_counts(self):
        query = """
        MATCH (n)
        RETURN labels(n)[0] AS type, count(*) AS count
        ORDER BY type
        """
        return self.run_query(query)

    def get_relationship_counts(self):
        query = """
        MATCH ()-[r]->()
        RETURN type(r) AS relationship, count(*) AS count
        ORDER BY relationship
        """
        return self.run_query(query)

    def get_all_suppliers(self):
        query = "MATCH (s:Supplier) RETURN s.name AS name, s.country AS country, s.industry AS industry"
        return self.run_query(query)

    def get_downstream_path(self, node_name, max_hops=4):
        """Trace the ripple path from a given node (e.g. a Supplier) downstream to Retailers."""
        query = f"""
        MATCH path = (start {{name: $node_name}})-[*1..{max_hops}]->(end:Retailer)
        RETURN [n IN nodes(path) | n.name] AS path_nodes
        """
        return self.run_query(query, {"node_name": node_name})


if __name__ == "__main__":
    client = Neo4jClient()

    print("=== Node Counts ===")
    for row in client.get_node_counts():
        print(row)

    print("\n=== Relationship Counts ===")
    for row in client.get_relationship_counts():
        print(row)

    print("\n=== All Suppliers ===")
    for row in client.get_all_suppliers():
        print(row)

    print("\n=== Sample Ripple Path: Congo Cobalt Mines -> Retailer ===")
    for row in client.get_downstream_path("Congo Cobalt Mines"):
        print(" -> ".join(row["path_nodes"]))

    client.close()
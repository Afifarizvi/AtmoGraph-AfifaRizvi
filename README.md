# AtmoGraph 🌐

### Supply Chain Ripple Effect Predictor

AtmoGraph is an AI-powered system that predicts how localized supply chain disruptions (e.g., port strikes, factory shutdowns) ripple across global, interconnected industries — using Graph Neural Networks and real-time NLP.

## Problem Statement
Traditional supply chain predictive models rely on linear, isolated time-series data. They fail to understand complex global networks and cannot predict how a localized crisis in one industry affects entirely unrelated industries across the globe.

## Key Modules
- **Graph Database (Neo4j):** Stores the global supply chain network — suppliers, manufacturers, shipping routes.
- **NLP Ingestion Engine (spaCy / HuggingFace):** Scrapes live news feeds and extracts entities to identify disruptions.
- **Graph Neural Network (PyTorch Geometric):** Predicts the "ripple effect" of a disruption across multi-hop graph nodes.
- **Interactive Network UI (React + D3.js / React Flow):** Real-time visual dashboard of the supply chain graph.

## Tech Stack
- **Backend/ML:** Python, PyTorch Geometric, Neo4j, spaCy/HuggingFace, FastAPI
- **Frontend:** React, D3.js / React Flow
- **Real-time:** WebSockets

## Project Structure
AtmoGraph-AfifaRizvi/
├── backend/
│ ├── graph_db/ # Neo4j setup & Cypher scripts
│ ├── nlp_engine/ # NLP ingestion & entity extraction
│ └── gnn_model/ # Graph Neural Network (PyTorch Geometric)
├── frontend/
│ ├── src/ # React components
│ └── public/
└── docs/ # Project documentation

## Development Plan
| Week | Backend/ML | Frontend |
|------|-----------|----------|
| Week 1 | Neo4j setup, mock graph data, Cypher scripts | React scaffold, static graph render |
| Week 2 | NLP pipeline, NER, risk state updates | Interactive graph, node-click details |
| Week 3 | GNN training for delay prediction | Predictive overlay (at-risk nodes) |
| Week 4 | Real-time WebSocket/FastAPI integration | Timeline sliders, polish |

## Author
Afifa Rizvi — MSc IT, Mohanlal Sukhadia University
Internship Project @ Infotact Solutions
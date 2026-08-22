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

## Progress Log

### ✅ Week 1 — Complete (Days 1–6)

**Backend:**
- Neo4j AuraDB Free instance set up and connected via Python driver
- Reusable `Neo4jClient` class built with query helpers (node counts, relationship counts, ripple path traversal)
- Mock global supply chain graph seeded: **32 nodes** (10 Suppliers, 8 Manufacturers, 8 Ports, 6 Retailers) and **32 relationships** (SUPPLIES, SHIPS_VIA, ROUTES_TO, DELIVERS_TO) across Electronics, Automotive, and Pharmaceuticals industries
- Verified multi-hop ripple path querying (e.g. Supplier → Manufacturer → Port → Port → Retailer)

**Frontend:**
- React app scaffolded with Vite
- Dark-themed dashboard layout with header and graph container
- Static supply chain network visualized using React Flow, with labeled nodes and relationship edges, zoom/pan controls, and minimap

**Milestones achieved:** Graph Logic (NLP-ready data ingestion into Neo4j) and Visualization Validation (frontend renders interconnected graph data) — both Mid-Project Review requirements met ahead of schedule.

### ✅ Week 2 — Complete (Days 1–6)

**Backend (NLP Pipeline):**
- NLP environment set up with spaCy (`en_core_web_sm`) for Named Entity Recognition
- Structured entity extraction built: identifies locations (GPE), organizations (ORG), and disruption-related keywords (strike, shutdown, delay, shortage, etc.) from raw news text
- Negation handling added to avoid false positives (e.g. "no reported disruptions" correctly ignored)
- Entity-to-graph matching implemented: extracted organizations matched against Neo4j node names using exact + substring fallback matching (covers cases where NER misses smaller/lesser-known entities)
- End-to-end disruption pipeline built: **news text → entity extraction → Neo4j node matching → automatic risk_level update**, verified working (e.g. "Stuttgart Auto Factory" risk updated from `low` to `high` based on live text input)

**Frontend:**
- Node-click interactivity added to the React Flow graph — clicking a node opens a details panel showing type, country, industry, and risk level
- Risk-based node coloring implemented (green = low, yellow = medium, red = high) with a visual legend, so at-risk entities are identifiable at a glance without clicking

**Milestones achieved:** Full backend-to-frontend risk pipeline is functional — a disruption mentioned in text can be traced through NLP extraction, matched to the correct graph node, and reflected visually on the dashboard as a color change.

### 🔜 Week 3 — In Progress

- Graph Neural Network (PyTorch Geometric) to predict downstream delays based on upstream disruption features
- Predictive overlay refinement on the frontend based on ML predictions

## Author
Afifa Rizvi — MSc IT, Mohanlal Sukhadia University
Internship Project @ Infotact Solutions
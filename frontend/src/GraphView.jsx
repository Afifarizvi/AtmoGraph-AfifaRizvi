import { computeHopDistances, getProjectedRiskLevel } from './utils/ripplePropagation';
import { useState, useCallback, useEffect } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';

const riskStyles = {
  low: { background: '#d4edda', border: '2px solid #28a745' },
  medium: { background: '#fff3cd', border: '2px solid #ffc107' },
  high: { background: '#f8d7da', border: '2px solid #dc3545' },
};

function applyRiskStyling(nodes) {
  return nodes.map((node) => ({
    ...node,
    style: {
      ...riskStyles[node.data.risk_level],
      borderRadius: 6,
      padding: 4,
      fontWeight: node.data.risk_level === 'high' ? 600 : 400,
    },
  }));
}

// Simple auto-layout: arrange nodes in columns by type, since the API
// doesn't provide x/y positions (those were hardcoded in the old mock data).
function autoLayout(nodes) {
  const typeOrder = { Supplier: 0, Manufacturer: 1, Port: 2, Retailer: 3 };
  const columnCounts = {};

  return nodes.map((node) => {
    const col = typeOrder[node.data.type] ?? 0;
    const row = columnCounts[col] || 0;
    columnCounts[col] = row + 1;

    return {
      ...node,
      position: { x: col * 280, y: row * 120 },
      type: col === 0 ? 'input' : col === 3 ? 'output' : undefined,
    };
  });
}

function GraphView() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dayHorizon, setDayHorizon] = useState('now');
  const [rawNodes, setRawNodes] = useState([]);
  const [rawEdges, setRawEdges] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/graph')
      .then((res) => res.json())
      .then((data) => {
        const positioned = autoLayout(data.nodes);
        const styled = applyRiskStyling(positioned);
        setNodes(styled);
        setEdges(data.edges);
        setRawNodes(data.nodes);
        setRawEdges(data.edges);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError('Could not connect to backend API. Is it running?');
        setLoading(false);
      });
  }, [setNodes, setEdges]);

    useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8000/ws');

    ws.onopen = () => console.log('✅ WebSocket connected');

    ws.onmessage = (event) => {
      console.log('📩 WebSocket message received:', event.data);
      const message = JSON.parse(event.data);
      if (message.type === 'risk_update') {
        setNodes((currentNodes) => {
          const updatedNodes = currentNodes.map((node) => {
            const update = message.updated_nodes.find((u) => u.name === node.id);
            if (update) {
              console.log(`🔄 Updating node ${node.id} to risk ${update.risk_level}`);
              return {
                ...node,
                data: { ...node.data, risk_level: update.risk_level },
                style: {
                  ...riskStyles[update.risk_level],
                  borderRadius: 6,
                  padding: 4,
                  fontWeight: update.risk_level === 'high' ? 600 : 400,
                },
              };
            }
            setRawNodes((currentRawNodes) =>
              currentRawNodes.map((node) => {
                const update = message.updated_nodes.find((u) => u.name === node.id);
                if (update) {
                  return { ...node, data: { ...node.data, risk_level: update.risk_level } };
                }
                return node;
              })
            );
            return node;
          });
          return updatedNodes;
        });
      }
    };

    ws.onerror = (err) => console.error('❌ WebSocket error:', err);
    ws.onclose = () => console.log('🔌 WebSocket disconnected');

    return () => ws.close();
  }, [setNodes]);

    
  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node);
  }, []);

    useEffect(() => {
    if (rawNodes.length === 0) return;

    const distances = computeHopDistances(rawNodes, rawEdges);
    const positioned = autoLayout(rawNodes);

    const restyled = positioned.map((node) => {
      const projectedRisk = getProjectedRiskLevel(
        node.data.risk_level,
        distances[node.id],
        dayHorizon
      );
      return {
        ...node,
        data: { ...node.data, projected_risk: projectedRisk },
        style: {
          ...riskStyles[projectedRisk],
          borderRadius: 6,
          padding: 4,
          fontWeight: projectedRisk === 'high' ? 600 : 400,
        },
      };
    });

    setNodes(restyled);
  }, [dayHorizon, rawNodes, rawEdges, setNodes]);

  const closePanel = () => setSelectedNode(null);

  if (loading) {
    return <div className="placeholder-text">Loading graph from backend...</div>;
  }

  if (error) {
    return <div className="placeholder-text">{error}</div>;
  }

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative', display: 'flex' }}>
      <div style={{ flex: 1, height: '100%' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          fitView
        >
          <Background />
          <Controls />
          <MiniMap
            nodeColor={(node) => {
              const level = node.data?.risk_level;
              if (level === 'high') return '#dc3545';
              if (level === 'medium') return '#ffc107';
              return '#28a745';
            }}
          />
        </ReactFlow>
      </div>
        <div className="timeline-slider">
        <label>Time Horizon: <strong>{dayHorizon === 'now' ? 'Now' : `${dayHorizon} Days`}</strong></label>
        <input
          type="range"
          min="0"
          max="3"
          step="1"
          value={['now', 30, 60, 90].indexOf(dayHorizon)}
          onChange={(e) => setDayHorizon(['now', 30, 60, 90][e.target.value])}
        />
        <div className="timeline-marks">
          <span>Now</span>
          <span>30d</span>
          <span>60d</span>
          <span>90d</span>
        </div>
      </div>

      <div className="legend">
        <div className="legend-item"><span className="legend-dot low"></span> Low Risk</div>
        <div className="legend-item"><span className="legend-dot medium"></span> Medium Risk</div>
        <div className="legend-item"><span className="legend-dot high"></span> High Risk</div>
      </div>

      {selectedNode && (
        <div className="details-panel">
          <button className="close-btn" onClick={closePanel}>✕</button>
          <h2>{selectedNode.data.label}</h2>
          <div className="detail-row">
            <span className="detail-label">Type:</span>
            <span>{selectedNode.data.type}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Country:</span>
            <span>{selectedNode.data.country}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Industry:</span>
            <span>{selectedNode.data.industry}</span>
          </div>
          <div className="detail-row">
            <span className="detail-label">Risk Level:</span>
            <span className={`risk-badge risk-${selectedNode.data.risk_level}`}>
              {selectedNode.data.risk_level?.toUpperCase()}
            </span>
          </div>
          <div className="detail-row">
            <span className="detail-label">GNN Predicted Risk:</span>
            <span>{selectedNode.data.predicted_risk_score?.toFixed(4)}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default GraphView;
import { useState, useCallback, useMemo } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { initialNodes, initialEdges } from './data/mockGraphData';

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

function GraphView() {
  const styledInitialNodes = useMemo(() => applyRiskStyling(initialNodes), []);
  const [nodes, , onNodesChange] = useNodesState(styledInitialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNode, setSelectedNode] = useState(null);

  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node);
  }, []);

  const closePanel = () => setSelectedNode(null);

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
        </div>
      )}
    </div>
  );
}

export default GraphView;
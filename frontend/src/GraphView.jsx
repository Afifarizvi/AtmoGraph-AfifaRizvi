import { useState, useCallback } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { initialNodes, initialEdges } from './data/mockGraphData';

function GraphView() {
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
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
          <MiniMap />
        </ReactFlow>
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
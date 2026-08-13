export const initialNodes = [
  // Suppliers
  { id: 'supplier-1', data: { label: 'Taiwan Semiconductor Co' }, position: { x: 0, y: 0 }, type: 'input' },
  { id: 'supplier-2', data: { label: 'Congo Cobalt Mines' }, position: { x: 0, y: 100 }, type: 'input' },
  { id: 'supplier-3', data: { label: 'Germany AutoParts GmbH' }, position: { x: 0, y: 300 }, type: 'input' },

  // Manufacturers
  { id: 'mfg-1', data: { label: 'Shenzhen Electronics Factory' }, position: { x: 250, y: 50 } },
  { id: 'mfg-2', data: { label: 'Stuttgart Auto Factory' }, position: { x: 250, y: 300 } },

  // Ports
  { id: 'port-1', data: { label: 'Port of Shanghai' }, position: { x: 500, y: 50 } },
  { id: 'port-2', data: { label: 'Port of Rotterdam' }, position: { x: 500, y: 300 } },
  { id: 'port-3', data: { label: 'Port of Los Angeles' }, position: { x: 750, y: 50 } },
  { id: 'port-4', data: { label: 'Port of Baltimore' }, position: { x: 750, y: 300 } },

  // Retailers
  { id: 'retailer-1', data: { label: 'North America Consumer Electronics Market' }, position: { x: 1000, y: 0 }, type: 'output' },
  { id: 'retailer-2', data: { label: 'North America Auto Market' }, position: { x: 1000, y: 200 }, type: 'output' },
  { id: 'retailer-3', data: { label: 'EU Auto Dealership Network' }, position: { x: 500, y: 450 }, type: 'output' },
];

export const initialEdges = [
  { id: 'e1', source: 'supplier-1', target: 'mfg-1', label: 'SUPPLIES' },
  { id: 'e2', source: 'supplier-2', target: 'mfg-1', label: 'SUPPLIES' },
  { id: 'e3', source: 'supplier-3', target: 'mfg-2', label: 'SUPPLIES' },
  { id: 'e4', source: 'mfg-1', target: 'port-1', label: 'SHIPS_VIA' },
  { id: 'e5', source: 'mfg-2', target: 'port-2', label: 'SHIPS_VIA' },
  { id: 'e6', source: 'port-1', target: 'port-3', label: 'ROUTES_TO' },
  { id: 'e7', source: 'port-2', target: 'port-4', label: 'ROUTES_TO' },
  { id: 'e8', source: 'port-3', target: 'retailer-1', label: 'DELIVERS_TO' },
  { id: 'e9', source: 'port-4', target: 'retailer-2', label: 'DELIVERS_TO' },
  { id: 'e10', source: 'port-2', target: 'retailer-3', label: 'DELIVERS_TO' },
];
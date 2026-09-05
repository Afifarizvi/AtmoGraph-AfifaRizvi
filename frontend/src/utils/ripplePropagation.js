/**
 * Computes, for every node, the shortest hop distance to the nearest
 * currently high-risk node — using BFS across the graph (treating edges
 * as undirected, since disruption can ripple through the supply chain
 * in either direction of dependency).
 */
export function computeHopDistances(nodes, edges) {
  const highRiskIds = nodes
    .filter((n) => n.data.risk_level === 'high')
    .map((n) => n.id);

  // Build adjacency list (undirected)
  const adjacency = {};
  nodes.forEach((n) => (adjacency[n.id] = []));
  edges.forEach((e) => {
    adjacency[e.source]?.push(e.target);
    adjacency[e.target]?.push(e.source);
  });

  const distances = {};
  nodes.forEach((n) => (distances[n.id] = Infinity));

  // Multi-source BFS starting from all high-risk nodes at once
  const queue = [...highRiskIds];
  highRiskIds.forEach((id) => (distances[id] = 0));

  while (queue.length > 0) {
    const current = queue.shift();
    const currentDist = distances[current];

    (adjacency[current] || []).forEach((neighbor) => {
      if (distances[neighbor] > currentDist + 1) {
        distances[neighbor] = currentDist + 1;
        queue.push(neighbor);
      }
    });
  }

  return distances;
}

/**
 * Given hop distances and a selected time horizon, returns a projected
 * risk level per node: nodes within the "reach" of the selected day
 * range are shown as affected, with severity decaying by distance.
 */
export function getProjectedRiskLevel(baseRiskLevel, hopDistance, dayHorizon) {
  if (baseRiskLevel === 'high') return 'high'; // always show the source as high

  const reachByDay = { now: 0, 30: 1, 60: 2, 90: 3 };
  const reach = reachByDay[dayHorizon];

  if (hopDistance === 0) return 'high';
  if (hopDistance <= reach) {
    return hopDistance === reach ? 'medium' : 'high';
  }
  return baseRiskLevel; // unaffected at this time horizon
}
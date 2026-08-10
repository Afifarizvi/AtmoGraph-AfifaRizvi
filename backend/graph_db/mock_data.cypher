// ==== SUPPLIERS (10) ====
UNWIND [
  {name:'Taiwan Semiconductor Co', country:'Taiwan', industry:'Electronics'},
  {name:'Congo Cobalt Mines', country:'DR Congo', industry:'Electronics'},
  {name:'Chile Lithium Corp', country:'Chile', industry:'Electronics'},
  {name:'South Korea Display Panels', country:'South Korea', industry:'Electronics'},
  {name:'Germany AutoParts GmbH', country:'Germany', industry:'Automotive'},
  {name:'Japan Steel Corp', country:'Japan', industry:'Automotive'},
  {name:'Malaysia Rubber Co', country:'Malaysia', industry:'Automotive'},
  {name:'India API Manufacturers', country:'India', industry:'Pharmaceuticals'},
  {name:'Switzerland Pharma Chemicals', country:'Switzerland', industry:'Pharmaceuticals'},
  {name:'China Pharma Ingredients', country:'China', industry:'Pharmaceuticals'}
] AS supplier
MERGE (s:Supplier {name: supplier.name})
SET s.country = supplier.country, s.industry = supplier.industry, s.risk_level = 'low';

// ==== MANUFACTURERS (8) ====
UNWIND [
  {name:'Shenzhen Electronics Factory', country:'China', industry:'Electronics'},
  {name:'Vietnam Assembly Plant', country:'Vietnam', industry:'Electronics'},
  {name:'Mexico Electronics Hub', country:'Mexico', industry:'Electronics'},
  {name:'Stuttgart Auto Factory', country:'Germany', industry:'Automotive'},
  {name:'Toyota City Plant', country:'Japan', industry:'Automotive'},
  {name:'Detroit Auto Plant', country:'USA', industry:'Automotive'},
  {name:'Mumbai Pharma Labs', country:'India', industry:'Pharmaceuticals'},
  {name:'Basel Pharma Plant', country:'Switzerland', industry:'Pharmaceuticals'}
] AS mfg
MERGE (m:Manufacturer {name: mfg.name})
SET m.country = mfg.country, m.industry = mfg.industry, m.risk_level = 'low';

// ==== PORTS (8) ====
UNWIND [
  {name:'Port of Shanghai', country:'China'},
  {name:'Port of Ho Chi Minh', country:'Vietnam'},
  {name:'Port of Los Angeles', country:'USA'},
  {name:'Port of Rotterdam', country:'Netherlands'},
  {name:'Port of Yokohama', country:'Japan'},
  {name:'Port of Baltimore', country:'USA'},
  {name:'Port of Mumbai', country:'India'},
  {name:'Port of Singapore', country:'Singapore'}
] AS port
MERGE (p:Port {name: port.name})
SET p.country = port.country, p.risk_level = 'low';

// ==== RETAILERS / MARKETS (6) ====
UNWIND [
  {name:'North America Consumer Electronics Market', country:'USA', industry:'Electronics'},
  {name:'EU Electronics Retail Network', country:'Germany', industry:'Electronics'},
  {name:'North America Auto Market', country:'USA', industry:'Automotive'},
  {name:'EU Auto Dealership Network', country:'France', industry:'Automotive'},
  {name:'Global Pharma Distribution Hub', country:'Belgium', industry:'Pharmaceuticals'},
  {name:'Africa Health Supply Network', country:'Kenya', industry:'Pharmaceuticals'}
] AS retailer
MERGE (r:Retailer {name: retailer.name})
SET r.country = retailer.country, r.industry = retailer.industry, r.risk_level = 'low';

// ==== SUPPLIES relationships (Supplier -> Manufacturer) ====
UNWIND [
  {from:'Taiwan Semiconductor Co', to:'Shenzhen Electronics Factory'},
  {from:'Congo Cobalt Mines', to:'Shenzhen Electronics Factory'},
  {from:'Chile Lithium Corp', to:'Vietnam Assembly Plant'},
  {from:'South Korea Display Panels', to:'Mexico Electronics Hub'},
  {from:'Germany AutoParts GmbH', to:'Stuttgart Auto Factory'},
  {from:'Japan Steel Corp', to:'Toyota City Plant'},
  {from:'Malaysia Rubber Co', to:'Detroit Auto Plant'},
  {from:'India API Manufacturers', to:'Mumbai Pharma Labs'},
  {from:'Switzerland Pharma Chemicals', to:'Basel Pharma Plant'},
  {from:'China Pharma Ingredients', to:'Mumbai Pharma Labs'}
] AS rel
MATCH (s:Supplier {name: rel.from}), (m:Manufacturer {name: rel.to})
MERGE (s)-[:SUPPLIES]->(m);

// ==== SHIPS_VIA relationships (Manufacturer -> Port) ====
UNWIND [
  {from:'Shenzhen Electronics Factory', to:'Port of Shanghai'},
  {from:'Vietnam Assembly Plant', to:'Port of Ho Chi Minh'},
  {from:'Mexico Electronics Hub', to:'Port of Los Angeles'},
  {from:'Stuttgart Auto Factory', to:'Port of Rotterdam'},
  {from:'Toyota City Plant', to:'Port of Yokohama'},
  {from:'Detroit Auto Plant', to:'Port of Baltimore'},
  {from:'Mumbai Pharma Labs', to:'Port of Mumbai'},
  {from:'Basel Pharma Plant', to:'Port of Rotterdam'}
] AS rel
MATCH (m:Manufacturer {name: rel.from}), (p:Port {name: rel.to})
MERGE (m)-[:SHIPS_VIA]->(p);

// ==== ROUTES_TO relationships (Port -> Port, shipping lanes) ====
UNWIND [
  {from:'Port of Shanghai', to:'Port of Los Angeles'},
  {from:'Port of Ho Chi Minh', to:'Port of Los Angeles'},
  {from:'Port of Rotterdam', to:'Port of Baltimore'},
  {from:'Port of Yokohama', to:'Port of Baltimore'},
  {from:'Port of Mumbai', to:'Port of Singapore'},
  {from:'Port of Singapore', to:'Port of Rotterdam'}
] AS rel
MATCH (p1:Port {name: rel.from}), (p2:Port {name: rel.to})
MERGE (p1)-[:ROUTES_TO]->(p2);

// ==== DELIVERS_TO relationships (Port -> Retailer) ====
UNWIND [
  {from:'Port of Los Angeles', to:'North America Consumer Electronics Market'},
  {from:'Port of Los Angeles', to:'North America Auto Market'},
  {from:'Port of Baltimore', to:'North America Auto Market'},
  {from:'Port of Rotterdam', to:'EU Electronics Retail Network'},
  {from:'Port of Rotterdam', to:'EU Auto Dealership Network'},
  {from:'Port of Rotterdam', to:'Global Pharma Distribution Hub'},
  {from:'Port of Singapore', to:'Global Pharma Distribution Hub'},
  {from:'Port of Mumbai', to:'Africa Health Supply Network'}
] AS rel
MATCH (p:Port {name: rel.from}), (r:Retailer {name: rel.to})
MERGE (p)-[:DELIVERS_TO]->(r);
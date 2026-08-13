import './App.css'
import GraphView from './GraphView'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>AtmoGraph</h1>
        <p>Supply Chain Ripple Effect Predictor</p>
      </header>

      <main className="dashboard">
        <div className="graph-container">
          <GraphView />
        </div>
      </main>
    </div>
  )
}

export default App
// workspare/Final-project/app/frontend/src/App.js
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>DevOps Final Project</h1>
        <p>A simple React App served via Nginx.</p>
        <p>This application will be deployed on AWS EKS using a full CI/CD pipeline.</p>
        <h2>Todo List (Static Example)</h2>
        <ul>
          <li>Learn Docker</li>
          <li>Learn Kubernetes</li>
          <li>Build a full CI/CD pipeline</li>
        </ul>
      </header>
    </div>
  );
}

// Minimal CSS
const style = document.createElement('style');
style.innerHTML = `
.App { text-align: center; }
.App-header { background-color: #282c34; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: calc(10px + 2vmin); color: white; }
ul { list-style: none; padding: 0; }
li { background: #444; margin: 5px; padding: 10px; border-radius: 5px; }
`;
document.head.appendChild(style);


export default App;

// workspare/Final-project/app/backend/src/index.js
const express = require('express');
const app = express();
const port = process.env.PORT || 3001;

app.get('/', (req, res) => {
  res.send({ message: 'Hello from the Backend!' });
});

app.get('/todos', (req, res) => {
  // Trả về một danh sách todo giả
  res.json([
    { id: 1, text: 'Learn Docker', completed: true },
    { id: 2, text: 'Learn Kubernetes', completed: true },
    { id: 3, text: 'Build a full CI/CD pipeline', completed: false },
  ]);
});

app.listen(port, () => {
  console.log(`Backend listening at http://localhost:${port}`);
});

const express = require('express');
const app = express();
const PORT = 8080;

app.get('/', (req, res) => {
  res.send('Hello from Docker Container!');
});

app.listen(PORT, () => {
  console.log(`App is running on port ${PORT}`);
});

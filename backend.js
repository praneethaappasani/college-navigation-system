/ === Backend: Node.js with Express ===

const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const app = express();
app.use(bodyParser.json());

// MongoDB Schema
const locationSchema = new mongoose.Schema({
  name: String,
  neighbors: [
    {
      target: String,
      distance: Number
    }
  ]
});
const Location = mongoose.model('Location', locationSchema);

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/collegeNavigation', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

// A* Algorithm Implementation
function aStar(graph, start, goal) {
  const heuristic = (a, b) => Math.abs(a.charCodeAt(0) - b.charCodeAt(0)); // Example heuristic

  let openSet = [start];
  let cameFrom = {};
  let gScore = { [start]: 0 };
  let fScore = { [start]: heuristic(start, goal) };

  while (openSet.length > 0) {
    openSet.sort((a, b) => fScore[a] - fScore[b]);
    let current = openSet.shift();

    if (current === goal) {
      let path = [];
      while (current in cameFrom) {
        path.unshift(current);
        current = cameFrom[current];
      }
      return { path: [start, ...path], cost: gScore[goal] };
    }

    let neighbors = graph[current] || [];
    for (let { target, distance } of neighbors) {
      let tentativeGScore = gScore[current] + distance;
      if (tentativeGScore < (gScore[target] || Infinity)) {
        cameFrom[target] = current;
        gScore[target] = tentativeGScore;
        fScore[target] = gScore[target] + heuristic(target, goal);
        if (!openSet.includes(target)) openSet.push(target);
      }
    }
  }

  return { path: [], cost: Infinity }; // No path found
}

// API Endpoints
app.post('/find-path', async (req, res) => {
  const { source, destination } = req.body;
  const locations = await Location.find({});

  // Build graph
  let graph = {};
  locations.forEach(loc => {
    graph[loc.name] = loc.neighbors;
  });

  const result = aStar(graph, source, destination);
  res.json(result);
});

app.get('/locations', async (req, res) => {
  const locations = await Location.find();
  res.json(locations);
});

app.post('/update-layout', async (req, res) => {
  const { name, neighbors } = req.body;
  const location = new Location({ name, neighbors });
  await location.save();
  res.json({ message: 'Location added successfully!' });
});

app.listen(3000, () => console.log('Backend running on port 3000'));

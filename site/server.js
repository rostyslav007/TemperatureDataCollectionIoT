const express = require('express');
const { Pool } = require('pg');
const cors = require('cors'); // To enable cross-origin requests

const app = express();
const port = 3000;

// Enable CORS for the frontend to access the API
app.use(cors());

// Create a PostgreSQL connection pool
const pool = new Pool({
  user: process.env.PG_USER, // replace with your DB username
  host: 'db', // replace with your DB host (e.g., 'localhost' or a cloud database URL)
  database: 'temperature', // replace with your database name
  password: process.env.PG_PASS, // replace with your DB password
  port: 5432, // PostgreSQL default port
});

// Endpoint to get temperature data from the database
app.get('/data', async (req, res) => {
  try {
    // SQL query to fetch timestamp and temperature, ordered by timestamp
    const query = 'SELECT datetime, temp FROM history ORDER BY datetime ASC';
    const result = await pool.query(query);

    // Send the results as JSON
    res.json(result.rows);
  } catch (err) {
    console.error('Error executing query:', err);
    res.status(500).send({ error: 'Database query failed' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

const express = require('express');
const app = express();
const pool = require('./databsepostgreSQL');
const allowCors = (
    req,
    res,
    next
  ) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header(
      'Access-Control-Allow-Headers',
      'Origin, X-Requested-With, Content-Type, Accept, Authorization, apikey, x-access-token'
    );
    next();
  }

app.use(allowCors);

app.use(express.json()) // => req.body


// Routes
app.get("/", async (req, res) => {
    try {
        const allEntries = await pool.query("SELECT * FROM notfälle ORDER BY date DESC");
        res.json(allEntries.rows);
    } catch (err) {
        console.log(err.message);
    }
})

app.listen(8080, () => console.log('Listening on Port 8080...'))


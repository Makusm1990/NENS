const express = require('express');
const app = express();
const pool = require('./databsepostgreSQL');
const { readFileSync, readFile } = require('fs');
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
    res.header('referrer-policy', 'no-referrer');
    next();
  }

app.use(allowCors);

app.use(express.json()) // => req.body

app.get("/config", async (req, res) => {
  const data = readFileSync('//dc01/netlogon/Notfall/configure.json');
  res.json(JSON.parse(data));

})


// Routes
app.get("/", async (req, res) => {
  try {
    const allEntries = await pool.query("SELECT * FROM notfälle ORDER BY date DESC");
    res.json(allEntries.rows);
  } catch (err) {
    console.log(err.message);
    }
})

// Route Notfall ID
app.param('id', function(req,res, next, id) {
  const modified = id;
  req.id = modified;
  next();
})

app.get("/Notfall_ID/:id", async (req, res) => {
  try {
    const allEntries = await pool.query("SELECT * FROM notfälle WHERE id=$1", [req.params.id]);
    //console.log(allEntries)
    res.json(allEntries.rows[0]);
  } catch (err) {
    console.log(err.message);
    }
})






// app listen
app.listen(8080, () => console.log('Listening on Port 8080...'))


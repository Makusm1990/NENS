const Pool = require("pg").Pool;

const pool = new Pool({
    host: "localhost",
    user: "postgres",
    port: "5432",
    password: "GesineBusdie1.",
    database: "Notfall"
})

module.exports = pool;
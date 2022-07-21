const Pool = require('pg').Pool;
const pool = new Pool({
  user: 'postgres',
  host: '10.10.4.240',
  database: 'Notfall',
  password: 'PraX1s',
  port: 5432,
});

module.exports = pool;
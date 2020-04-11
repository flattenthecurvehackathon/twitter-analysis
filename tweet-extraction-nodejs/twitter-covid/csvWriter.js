const { writeFileSync } = require('fs');
const { parse } = require('json2csv');

const fields = [
  'id',
  'id_str',
  'full_text',
  'created_at',
  'user_id',
  'user_id_str',
  'user_name',
  'user_screen_name',
  'user_location',
  'geo_town',
  'geo_state',
  'geo_coord',
  'neg',
  'neu',
  'pos',
  'compound'
];

function writeCSV(jsonData, filename, fieldsArr = fields) {
  const opts = { fieldsArr };
  const csv = parse(jsonData, opts);
  writeFileSync(
    `./output/${filename}.csv`,
    Buffer.from(csv)
  )
}

module.exports = {
  writeCSV
};

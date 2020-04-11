const csv = require('jquery-csv');
const fs = require('fs');
const { locations } = require('./locations');
const { writeCSV } = require('./csvWriter');

const sample = './raw-data/vic-cases.csv';
let casesJson = [];

fs.readFile(sample, 'UTF-8', (err, fileContent) => {
  csv.toObjects(fileContent, {}, (err, cases) => {
    locations.forEach(loc => {
      const casesFromLocation = cases.filter(
        c => c.town.match(new RegExp(loc.town, 'i')));
      if (casesFromLocation.length > 0) {
        console.log(`${casesFromLocation[0].num_cases} cases in ${loc.town}`);
        // console.log(`${casesFromLocation.length} cases in ${loc.town}`);
        casesJson.push({ town: loc.town, num_cases: casesFromLocation[0].num_cases });
        // casesJson.push({ town: loc.town, num_cases: casesFromLocation.length });
      }
    });
    writeCSV(casesJson, 'vic-cases', ['town', 'num_cases'])
  });
});

const vader = require('vader-sentiment');
const csv = require('jquery-csv');
const fs = require('fs');

fs.readFile('./output/1.csv', 'UTF-8', (err, fileContent) => {
  csv.toObjects(fileContent, {}, (err, cases) => {
    cases.map(c => {
      const intensity = vader.SentimentIntensityAnalyzer.polarity_scores(c.full_text);
      console.log(`${c.full_text}  ${JSON.stringify(intensity)}`)
    })
  })
});


const hashtags = [
  'coronavirusaus',
  'pandemic',
  'covid-19',
  'covid',
  'Stressed',
  'lockdown',
  'Job loss',
  'Unemployed',
  'Broke',
];

function getHashtagQuery() {
  return encodeURIComponent(`#${hashtags.join(' OR #')}`)
}

module.exports = {
  getHashtagQuery,
};

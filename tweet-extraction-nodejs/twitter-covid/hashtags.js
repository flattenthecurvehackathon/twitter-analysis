const hashtags = [
  'coronavirus',
  'coronavirusaus',
  'covid19',
  'covid_19',
  'covid'
];

function getHashtagQuery() {
  return encodeURIComponent(`#${hashtags.join(' OR #')}`)
}

module.exports = {
  getHashtagQuery,
};

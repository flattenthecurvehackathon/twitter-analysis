require('isomorphic-fetch');
const qs = require('querystring');
const base64 = data => Buffer.from(data).toString('base64');

const consumerKey = 'PokylTekMorM4cDpegEm4HEOJ';
const consumerSecret = process.env.CONSUMER_SECRET;
const consumerKeySecretBase64 = base64(`${consumerKey}:${consumerSecret}`);

const query = qs.stringify({
  '#': 'covid',
  'result_type': 'recent',
  geocode: '-25.2743988,133.7751312,10000km', // 10,000km radius from centre of australia
  lang: 'en'
});

fetch('https://api.twitter.com/oauth2/token', {
  method: 'POST',
  headers: {
    Authorization: `Basic ${consumerKeySecretBase64}`,
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Content-Length': 29,
    'Accept-Encoding': 'gzip',
  },
  body: `grant_type=client_credentials`,
})
  .then(res => res.json())
  .then(json =>
    fetch(`https://api.twitter.com/1.1/search/tweets.json?q=${query}`, {
        headers: {
          'Content-Type': 'application/json',
          'Accept-Encoding': 'gzip',
          Authorization: `Bearer ${json.access_token}`,
        },
      }),
  )
  .then(res => res.json())
  .then(console.log);

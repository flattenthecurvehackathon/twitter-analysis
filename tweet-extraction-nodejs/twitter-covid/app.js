require('isomorphic-fetch');
const qs = require('querystring');
const hashtags = require('./hashtags');
const base64 = data => Buffer.from(data).toString('base64');
const fs = require('fs');

const consumerKey = 'PokylTekMorM4cDpegEm4HEOJ';
const consumerSecret = process.env.CONSUMER_SECRET;
const consumerKeySecretBase64 = base64(`${consumerKey}:${consumerSecret}`);

const query = qs.stringify({
  // 'result_type': 'recent',
  // geocode: '-25.2743988,133.7751312,10000km', // 10,000km radius from centre of australia
  geocode: '-37.840935,144.946457,10km', // melbourne
  lang: 'en',
  count: 100,
  'tweet_mode': 'extended'
});

let accumTweets = [];

function fetchNextResultsPage(nextResultsQueryString, access_token, iteration) {
  console.log(`requesting iteration ${iteration}`);
  return fetch(
    `https://api.twitter.com/1.1/search/tweets.json?${nextResultsQueryString}`,
    {
      headers: {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip',
        Authorization: `Bearer ${access_token}`,
      },
    })
    .then(res => res.json())
    .then(resJson => {
      accumTweets.push(...resJson.statuses.map(buildTweetObject));
      return resJson;
    })
    .then(json => {
      if (iteration > 0)
        return fetchNextResultsPage(json.search_metadata.next_results,
          access_token, iteration - 1);
    });
}

function getAccessToken() {
  return fetch('https://api.twitter.com/oauth2/token', {
    method: 'POST',
    headers: {
      Authorization: `Basic ${consumerKeySecretBase64}`,
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      'Content-Length': 29,
      'Accept-Encoding': 'gzip',
    },
    body: `grant_type=client_credentials`,
  }).then(res => res.json());
}

const filterRetweets = encodeURIComponent('-filter:retweets');

console.log(`https://api.twitter.com/1.1/search/tweets.json?q=${hashtags.getHashtagQuery()}&${query}`);

getAccessToken()
  .then(({ access_token }) =>
    fetch(
      `https://api.twitter.com/1.1/search/tweets.json?q=${hashtags.getHashtagQuery()}${filterRetweets}&${query}`,
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept-Encoding': 'gzip',
          Authorization: `Bearer ${access_token}`,
        },
      })
      .then(res => res.json())
      .then(resJson => {
        accumTweets.push(...resJson.statuses.map(buildTweetObject));
        return resJson;
      })
      .then(async json => await fetchNextResultsPage(
        json.search_metadata.next_results, access_token, 0))
      .then(() => fs.writeFileSync('./output/tweets.json', Buffer.from(JSON.stringify(accumTweets)))),
  );

function buildTweetObject({user: {id: user_id, id_str: user_id_str, name, screen_name, location}, text, full_text, id, id_str}) {
  return {
    id,
    id_str,
    text,
    full_text,
    user: {user_id, user_id_str, name, screen_name, location},
  }
}

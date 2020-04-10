require('isomorphic-fetch');
const qs = require('querystring');
const hashtags = require('./hashtags');
const { writeCSV } = require('./csvWriter');
const { locations } = require('./locations');
const base64 = data => Buffer.from(data).toString('base64');

const consumerKey = 'PokylTekMorM4cDpegEm4HEOJ';
const consumerSecret = process.env.CONSUMER_SECRET;
const consumerKeySecretBase64 = base64(`${consumerKey}:${consumerSecret}`);

const query = qs.stringify({
  'result_type': 'recent',
  lang: 'en',
  count: 100,
  'tweet_mode': 'extended'
});

async function fetchNextResultsPage(nextResultsQueryString, access_token, iteration, {town, state, coord}, accumTweets) {
  console.log(`requesting iteration ${iteration}, town ${town}`);
  return await fetch(
    `https://api.twitter.com/1.1/search/tweets.json?${nextResultsQueryString}`,
    {
      headers: {
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip',
        Authorization: `Bearer ${access_token}`,
      },
    })
    .then(res => res.json())
    .then(async json => {
      if (iteration > 0 && json.search_metadata && json.search_metadata.next_results) {
        const tweetsSoFar = [
          ...json.statuses.map(
            tweet => buildTweetObject(tweet, town, state, coord)),
          ...accumTweets];
        return await fetchNextResultsPage(json.search_metadata.next_results,
          access_token, iteration - 1, { town, state, coord }, tweetsSoFar);
      } else {
        return accumTweets;
      }
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
const buildQuery = (coord) => `q=${hashtags.getHashtagQuery()}${filterRetweets}&${query}&geocode=${coord},10km`;

getAccessToken()
  .then(({ access_token }) =>
    locations.forEach(async loc =>
      await fetchNextResultsPage(buildQuery(loc.coord), access_token, 10, loc, [])
        .then((accumTweets) =>
          writeCSV(accumTweets, `${loc.town}_${loc.state}`)
        ),
    ),
  );

function buildTweetObject({ user: { id: user_id, id_str: user_id_str, name: user_name, screen_name: user_screen_name, location: user_location }, full_text, id, id_str, created_at }, geo_town, geo_state, geo_coord) {
  return {
    id,
    id_str,
    full_text,
    created_at,
    user_id,
    user_id_str,
    user_name,
    user_screen_name,
    user_location,
    geo_town,
    geo_state,
    geo_coord
  }
}

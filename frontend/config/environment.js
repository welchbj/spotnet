/* jshint node: true */

module.exports = function(environment) {
  var ENV = {
    modulePrefix: 'frontend',
    environment: environment,
    rootURL: '/',
    locationType: 'auto',

    SPOTIFY_AUTH_BASE_URL: 'https://accounts.spotify.com/authorize',
    SPOTIFY_SCOPE: 'playlist-read-private user-library-read',
    SPOTIFY_WEB_API_HOST: 'https://api.spotify.com',
    SPOTIFY_WEB_API_NAMESPACE: '/v1',

    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. 'with-controller': true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false
      }
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    }
  };

  try {
    // Put the following in your local_config.js file:
    // exports.config = {
    //   SPOTIFY_CLIENT_ID: 'YOUR SPOTIFY CLIENT ID',
    //   SPOTIFY_AUTH_REDIRECT_URL: 'YOUR SPOTIFY AUTH REDIRECT URL'
    // };
    var local = require('./local_config.js');
    Object.keys(local.config).forEach(function(key) {
      ENV[key] = local.config[key];
    });
  } catch(err) {
    console.log('local_config.js file not found.');
  }

  if (environment === 'development') {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === 'test') {
    // Testem prefers this...
    ENV.locationType = 'none';

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = '#ember-testing';
  }

  if (environment === 'production') {

  }

  return ENV;
};

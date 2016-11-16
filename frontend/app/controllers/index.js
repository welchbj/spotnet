import Ember from 'ember';
import config from '../config/environment';

export default Ember.Controller.extend({

  spotifyAuthRequestUrl: (
    config.SPOTIFY_AUTH_BASE_URL +
    '?client_id=' +
    config.SPOTIFY_CLIENT_ID +
    '&response_type=token' +
    '&redirect_uri=' +
    encodeURIComponent(config.SPOTIFY_AUTH_REDIRECT_URL) +
    '&scope=' +
    encodeURIComponent(config.SPOTIFY_SCOPE))

});

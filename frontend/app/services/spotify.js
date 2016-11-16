import Ember from 'ember';
import SpotifyClient from 'npm:spotify-web-api-js';
import { storageFor } from 'ember-local-storage';

/**
 * The client-side Spotify service, used to manage
 * the Spotify session and interact with the Spotify
 * Web API.
 */
export default Ember.Service.extend({

  /**
   * Local storage for access tokens.
   */
  tokens: storageFor('tokens'),

  /**
   * Returns whether the service thinks it holds a valid
   * authentication token.
   */
  isAuthenticated: false,

  /**
   * The in-memory Spotify API access token.
   */
  accessToken: null,

  /**
   * The client for interacting with the Spotify Web API, from the
   * spotify-web-api-js package.
   */
  client: null,

  init() {
    this._super(...arguments);
    this.loadClient();
    this.loadToken();
  },

  /**
   * Set the in-memory access token, write it to local storage, and mark
   * the Spotify session as authenticated.
   */
  setToken(token) {
    this.setProperties({
      'accessToken': token,
      'tokens.spotifyAccessToken': token,
      'isAuthenticated': token !== null
    });

    this.get('client').setAccessToken(token);
  },

  /**
   * Load the stored Spotify access token from local storage. One may not be
   * present, in which case accessToken will be null.
   */
  loadToken() {
    this.setToken(this.get('tokens.spotifyAccessToken'));
  },

  loadClient() {
    const client = new SpotifyClient();
    client.setPromiseImplementation(Ember.RSVP.Promise);

    const token = this.get('token');
    if (token !== null) {
      client.setAccessToken(token);
    }

    this.set('client', client);
  }

});

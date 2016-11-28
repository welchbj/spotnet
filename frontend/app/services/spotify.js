import Ember from 'ember';
import { storageFor } from 'ember-local-storage';

/**
 * The client-side Spotify service, used to manage
 * the Spotify session and interact with the Spotify
 * Web API.
 */
export default Ember.Service.extend({

  /**
   * Ajax service for making backend requests to the
   * Spotify Web API.
   */
  ajax: Ember.inject.service(),

  /**
   * Local storage for access tokens.
   */
  tokens: storageFor('tokens'),

  /**
   * The in-memory Spotify API access token.
   */
  accessToken: null,

  /**
   * Computed property that returns whether the service thinks
   * it holds a valid authentication token.
   */
  isAuthenticated: Ember.computed('accessToken', function() {
    return this.get('accessToken') !== null;
  }),

  init() {
    this._super(...arguments);
    this.loadToken();
  },

  /**
   * Set the in-memory access token, write it to local storage, and mark
   * the Spotify session as authenticated.
   */
  setToken(token) {
    this.setProperties({
      'accessToken': token,
      'tokens.spotifyAccessToken': token
    });
  },

  /**
   * Load the stored Spotify access token from local storage. One may not be
   * present, in which case accessToken will be null.
   */
  loadToken() {
    this.setToken(this.get('tokens.spotifyAccessToken'));
  },

  /**
   * Remove the current Spotify access token from both in-memory
   * and local storage, setting it to null.
   */
  invalidateToken() {
    this.setToken(null);
  },

  /**
   * Returns a promise from the Spotify Web API /me endpoint.
   */
  getMe() {
    return this.get('ajax').request('/me');
  },

  /**
   * TODO
   */
  getPlaylists() {
    // TODO
  },

  /**
   * TODO
   */
  getTracks(pageNumber) {
    // TODO
  }

});

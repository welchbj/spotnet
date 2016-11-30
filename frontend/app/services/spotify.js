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
   * Get the user's playlists, indicating the page of the paginated list
   * of playlists to get and the the number of playlists on each page.
   */
  getPlaylists(page, playlistsPerPage) {
    const endpoint = '/me/playlists?offset=' + (page * playlistsPerPage) +
                     '&limit=' + playlistsPerPage;
    return this.get('ajax').request(endpoint);
  },

  /**
   * Get metadata information about a playlist. This will make a request
   * to get the following fields from the playlist object:
   *    description
   *    followers
   *    name
   */
  getPlaylistMetadata(userId, playlistId) {
    const endpoint = `/users/${userId}/playlists/${playlistId}`;
    const params = '?fields=description,followers,name';
    return this.get('ajax').request(endpoint + params);
  },

  /**
   * Get the tracks for a user's playlist, indicating the page to get
   * as well as the number of entries which should be on each page.
   */
  getTracksFromPlaylist(userId, playlistId, page, tracksPerPage) {
    const endpoint = `/users/${userId}/playlists/${playlistId}/tracks`;
    const params = `?offset=${page * tracksPerPage}&limit=${tracksPerPage}`;
    return this.get('ajax').request(endpoint + params);
  },

  /**
   * Get the user's saved tracks, indicating the page of the paginated list
   * of songs to get and the number of tracks on each page.
   */
  getTracks(page, tracksPerPage) {
    const endpoint = '/me/tracks?offset=' + (page * tracksPerPage) +
                     '&limit=' + tracksPerPage;
    return this.get('ajax').request(endpoint);
  }

});

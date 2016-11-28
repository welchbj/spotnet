import AjaxService from 'ember-ajax/services/ajax';
import Ember from 'ember';
import ENV from '../config/environment';

/**
 * Ajax service for interacting with the Spotify
 * Web API backend.
 */
export default AjaxService.extend({

  spotify: Ember.inject.service(),

  host: ENV.SPOTIFY_WEB_API_HOST,

  namespace: ENV.SPOTIFY_WEB_API_NAMESPACE,

  headers: Ember.computed('spotify.accessToken', {
    get() {
      let headers = {};
      const accessToken = this.get('spotify.accessToken');

      if (accessToken) {
        headers['Authorization'] = 'Bearer ' + accessToken;
      } else {
        console.log('No access token for Spotify; something will probably ' +
                    'go wrong soon.');
      }

      return headers;
    }
  })

});

import DS from 'ember-data';
import Ember from 'ember';
import ENV from '../config/environment';

export default DS.JSONAPIAdapter.extend({

  spotify: Ember.inject.service(),

  host: ENV.SPOTIFY_WEB_API_HOST,

  namespace: ENV.SPOTIFY_WEB_API_NAMESPACE,

  baseUrl: Ember.computed('host', 'namespace', function() {
    const host = this.get('host');
    const namespace = this.get('namespace');
    return `${host}${namespace}`;
  }),

  headers: Ember.computed('spotify.accessToken', {
    get() {
      let headers = {};
      const accessToken = this.get('spotify.accessToken');

      if (accessToken) {
        headers['Authorization'] = 'Bearer ' + accessToken;
      }
      else {
        console.log('No access token for Spotify; something will probably ' +
                    'go wrong soon.');
      }

      return headers;
    }
  })

});

import Ember from 'ember';

/**
 * A component for rendering user info; specifically,
 * the data resulting from Spotify's /me endpoint.
 */
export default Ember.Component.extend({

  /**
   * The user JSON object returned from the /me endpoint.
   */
  user: null,

  userName: Ember.computed('user', function() {
    const userObj = this.get('user');
    return userObj == null ? null : userObj['display_name'];
  }),

  spotifyProfileUrl: Ember.computed('user', function() {
    const userObj = this.get('user');
    return userObj == null ? null : userObj['external_urls']['spotify'];
  }),

  imageUrl: Ember.computed('user', function() {
    const userObj = this.get('user');
    return userObj == null ? null : userObj['images'][0]['url'];
  })

});

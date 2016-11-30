import Ember from 'ember';

/**
 * A component for rendering user info; specifically,
 * the data resulting from Spotify's /me endpoint.
 */
export default Ember.Component.extend({

  /**
   * The user model, processed from the Spotify Web API's /me endpoint.
   */
  user: null

});

import Ember from 'ember';

/**
 * Controller for the /auth route, handling query
 * parameters returned from the Spotify authentication
 * flow and validating/redirecting appropriately.
 */
export default Ember.Controller.extend({

  queryParams: {
    error: 'error'
  },

  error: null

});

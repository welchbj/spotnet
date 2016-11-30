import Ember from 'ember';

export default Ember.Component.extend({

  classNames: ['item'],

  /**
   * A track model representing a Spotify song/track, derived from the Spotify
   * Web API.
   */
  song: null

});

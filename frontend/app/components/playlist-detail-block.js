import Ember from 'ember';

export default Ember.Component.extend({

  classNames: ['item'],

  /**
   * A playlist model, derived from Spotify's Web API.
   */
  playlist: null

});

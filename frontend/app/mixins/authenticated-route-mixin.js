import Ember from 'ember';

export default Ember.Mixin.create({

  spotify: Ember.inject.service(),

  /**
   * Redirect to the index if the Spotify service is not authenticated.
   */
  beforeModel() {
    if (!this.get('spotify.isAuthenticated')) {
      this.transitionTo('index', {
        queryParams: {
          msgId: 'NEED_TO_CONNECT_ACCOUNT'
        }
      });
    }
  }

});

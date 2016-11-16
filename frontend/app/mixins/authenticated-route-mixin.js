import Ember from 'ember';

export default Ember.Mixin.create({

  spotify: Ember.inject.service(),

  /**
   * Redirect to the index if the Spotify service is not authenticated.
   */
  beforeModel() {
    if (!this.get('spotify.isAuthenticated')) {
      // TODO: need message about unauthenticated status
      this.transitionTo('index');
    }
  }

});

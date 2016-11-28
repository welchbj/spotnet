import Ember from 'ember';

export default Ember.Route.extend({

  spotify: Ember.inject.service(),

  beforeModel() {
    this.get('spotify').invalidateToken();
    this.transitionTo('index', {
      queryParams: {
        msgId: 'DISCONNECTED_ACCOUNT'
      }
    });
  }

});

import Ember from 'ember';

export default Ember.Controller.extend({

  spotnet: Ember.inject.service(),

  spotnetHadError: Ember.observer('spotnet.wasConnectionError', function() {
    if (this.get('spotnet.wasConnectionError')) {
      this.transitionToRoute('index', {
        queryParams: {
          msgId: 'SPOTNET_MASTER_CONNECTION_FAILED'
        }
      });
    }
  })

});

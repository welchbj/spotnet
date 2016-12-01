import Ember from 'ember';

export default Ember.Route.extend({

  actions: {
    error(error, transition) {  // jshint ignore:line
      if (error) {
        Ember.Logger.log(error);

        return this.transitionTo('index', {
          queryParams: {
            msgId: 'ERROR_NETWORK_REQUEST'
          }
        });
      }
    }
  }

});

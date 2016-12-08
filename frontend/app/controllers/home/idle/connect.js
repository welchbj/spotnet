import Ember from 'ember';

export default Ember.Controller.extend({

  spotnet: Ember.inject.service(),

  actions: {

    setIdle(slave) {
      Ember.set(slave, 'loginStatus', 'idle');
    }


  }

});

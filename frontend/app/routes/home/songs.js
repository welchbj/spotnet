import Ember from 'ember';

export default Ember.Route.extend({

  queryParams: {
    page: {
      refreshModel: true
    }
  },

  spotify: Ember.inject.service(),

  beforeModel() {
    this.controllerFor('home').set('activeTab', 'songs');
  },

  model(params) {
    return this.get('spotify').getTracks(params.page - 1, 10);
  }

});

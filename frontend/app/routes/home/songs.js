import Ember from 'ember';
import ENV from '../../config/environment';

export default Ember.Route.extend({

  queryParams: {
    page: {
      refreshModel: true
    }
  },

  spotify: Ember.inject.service(),

  model(params) {
    const limit = ENV.NUM_SONGS_PER_PAGE;
    const offset = (params.page - 1) * limit;

    return this.get('store').query('track', {
      tracksFrom: 'me',
      offset: offset,
      limit: limit
    });
  },

  afterModel() {
    this.controllerFor('home').set('activeTab', 'songs');
  }

});

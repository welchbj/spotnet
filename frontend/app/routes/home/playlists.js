import Ember from 'ember';
import ENV from '../../config/environment';

export default Ember.Route.extend({

  queryParams: {
    page: {
      refreshModel: true
    }
  },

  spotify: Ember.inject.service(),

  beforeModel() {
    this.controllerFor('home').set('activeTab', 'playlists');
  },

  model(params) {
    const limit = ENV.NUM_PLAYLISTS_PER_PAGE;
    const offset = (params.page - 1) * limit;

    return this.get('store').query('playlist', {
      offset: offset,
      limit: limit
    });
  }

});

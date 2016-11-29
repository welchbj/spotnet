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
    return this.get('spotify').getPlaylists(params.page - 1,
                                            ENV.NUM_PLAYLISTS_PER_PAGE);
  }

});

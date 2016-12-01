import Ember from 'ember';
import ENV from '../../config/environment';

export default Ember.Route.extend({

  queryParams: {
    q: {
      refreshModel: true
    },

    page: {
      refreshModel: true
    }
  },

  beforeModel() {
    this.controllerFor('home').set('activeTab', 'search');
  },

  model(params) {
    const { q, page } = params;
    if (!q) {
      return null;
    }

    const limit = ENV.NUM_SONGS_PER_PAGE;
    const offset = (page - 1) * limit;

    if (this.controller) {
      this.controller.set('isSearching', true);
    }
    return this.get('store').query('track', {
      tracksFrom: 'search',
      q: q,
      limit: limit,
      offset: offset
    }).then((result) => {
      if (this.controller) {
        this.controller.set('isSearching', false);
      }

      return result;
    });
  }

});

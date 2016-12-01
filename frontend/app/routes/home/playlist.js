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
    const store = this.get('store');
    const { page, owner_id, playlist_id } = params;

    const limit = ENV.NUM_SONGS_PER_PAGE;
    const offset = (page - 1) * limit;

    return Ember.RSVP.hash({
      playlist: store.findRecord('playlist', playlist_id, {
        adapterOptions: {
          ownerId: owner_id
        }
      }),
      tracks: store.query('track', {
        tracksFrom: 'playlist',
        ownerId: owner_id,
        playlistId: playlist_id,
        limit: limit,
        offset: offset
      })
    });
  }

});

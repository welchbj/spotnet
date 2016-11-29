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
    const spotify = this.get('spotify');
    const { page, owner_id, playlist_id } = params;

    return Ember.RSVP.hash({
      metadata: spotify.getPlaylistMetadata(owner_id, playlist_id),
      songs: spotify.getTracksFromPlaylist(owner_id, playlist_id, page - 1,
                                           ENV.NUM_SONGS_PER_PAGE)
    });
  }

});

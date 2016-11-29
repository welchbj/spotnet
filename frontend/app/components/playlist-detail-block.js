import Ember from 'ember';

export default Ember.Component.extend({

  classNames: ['item'],

  /**
   * A playlist object from Spotify's Web API.
   */
  playlist: null,

  playlistUrl: Ember.computed('playlist', function() {
    return this.get('playlist').external_urls.spotify;
  }),

  playlistName: Ember.computed('playlist', function() {
    return this.get('playlist').name;
  }),

  numPlaylistSongs: Ember.computed('playlist', function() {
    return this.get('playlist').tracks.total;
  }),

  playlistId: Ember.computed('playlist', function() {
    return this.get('playlist').id;
  })

});

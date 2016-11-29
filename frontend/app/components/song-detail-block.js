import Ember from 'ember';

export default Ember.Component.extend({

  classNames: ['item'],

  /**
   * A JSON object representing a song, from the Spotify Web API.
   */
  song: null,

  songName: Ember.computed('song', function() {
    return this.get('song').track.name;
  }),

  songUrl: Ember.computed('song', function() {
    return this.get('song').track.external_urls.spotify;
  }),

  albumName: Ember.computed('song', function() {
    return this.get('song').track.album.name;
  }),

  artistNames: Ember.computed('song', function() {
    const artistObjs = this.get('song').track.artists;
    const artistNameArray = artistObjs.getEach('name');
    return artistNameArray.join(', ');
  }),

  albumImageUrl: Ember.computed('song', function() {
    const imageObj = this.get('song').track.album.images[0];
    return imageObj === undefined  ? null : imageObj.url;
  }),

  /**
   * Since playlists can contain songs that were originally on someone's
   * local computer (and not playable from the Spotify service), this computed
   * property serves to indicate whether a song is playable via Spotify.
   * Songs not playable via spotify cannot be added to a queue.
   */
  isSpotifySong: Ember.computed('songUrl', function() {
    const songUrl = this.get('songUrl');
    return songUrl !== null && songUrl !== undefined;
  })

});

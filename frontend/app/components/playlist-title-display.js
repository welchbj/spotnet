import Ember from 'ember';

export default Ember.Component.extend({

  /**
   * The playlist model, derived from Spotify's Web API.
   */
  playlist: null,

  /**
   * The number of tracks contained within the playlist.
   */
  numTracks: null

});

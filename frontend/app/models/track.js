import attr from 'ember-data/attr';
import Ember from 'ember';
import Model from 'ember-data/model';

/**
 * A Spotify track model, derived from Spotify's Web API. See:
 * https://developer.spotify.com/web-api/get-track/
 */
export default Model.extend({

  artists: attr('string'),

  albumName: attr('string'),

  albumImageUrl: attr('string'),

  durationMs: attr('number'),

  spotifyUrl: attr('string'),

  name: attr('string'),

  spotifyUri: attr('string'),

  /**
   * Since playlists can contain songs that were originally on someone's
   * local computer (and not playable from the Spotify service), this computed
   * property serves to indicate whether a song is playable via Spotify.
   * Songs not playable via spotify cannot be added to a queue.
   */
  isSpotifyTrack: Ember.computed('spotifyUrl', function() {
    const url = this.get('spotifyUrl');
    return url !== null && url !== undefined;
  })

});

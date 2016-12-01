import Ember from 'ember';

export default Ember.Component.extend({

  classNames: ['item'],

  /**
   * A track model representing a Spotify song/track, derived from the Spotify
   * Web API.
   */
  song: null,

  descriptionText: Ember.computed('song', function() {
    const song = this.get('song');
    const albumName = song.get('albumName');
    const artists = song.get('artists');
    const duration = song.get('durationMinutesSeconds');

    return [albumName, artists, duration].filter((item) => item).join(' | ');
  })

});

import Ember from 'ember';

export default Ember.Component.extend({

  /**
   * The name of the playlist.
   */
  name: null,

  /**
   * The description of the playlist; this is commonly not present.
   */
  description: null,

  /**
   * The number of the playlist's followers.
   */
  numFollowers: null,

  /**
   * The number of songs contained in the playlist.
   */
  numSongs: null

});

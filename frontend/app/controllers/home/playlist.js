import Ember from 'ember';
import ENV from '../../config/environment';

export default Ember.Controller.extend({

  queryParams: ['page'],

  /**
   * The current page of songs to display.
   */
  page: 1,

  numSongs: Ember.computed('model', function() {
    return this.get('model').songs.total;
  }),

  numPages: Ember.computed('numSongs', function() {
    return Math.ceil(this.get('numSongs') / ENV.NUM_SONGS_PER_PAGE);
  })

});

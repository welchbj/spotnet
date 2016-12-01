import Ember from 'ember';
import ENV from '../../config/environment';

export default Ember.Controller.extend({

  queryParams: ['page'],

  /**
   * The current page of songs to display.
   */
  page: 1,

  numTracks: Ember.computed('model', function() {
    return this.get('model').tracks.meta.numTracks;
  }),

  numPages: Ember.computed('numTracks', function() {
    return Math.ceil(this.get('numTracks') / ENV.NUM_SONGS_PER_PAGE);
  })

});

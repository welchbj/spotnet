import Ember from 'ember';
import ENV from '../../config/environment';

export default Ember.Controller.extend({

  queryParams: ['page'],

  /**
   * The current page of songs to display.
   */
  page: 1,

  numPages: Ember.computed('model', function() {
    const numEntries = this.get('model').songs.total;
    return Math.ceil(numEntries / ENV.NUM_SONGS_PER_PAGE);
  })

});

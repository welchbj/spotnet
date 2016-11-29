import Ember from 'ember';
import ENV from '../../config/environment';

export default Ember.Controller.extend({

  queryParams: ['page'],

  /**
   * Query param to indicate current page in Spotify's API.
   */
  page: 1,

  /**
   * The total number of pages available for querying.
   */
  numPages: Ember.computed('model', function() {
    const numEntries = this.get('model').total;
    return Math.ceil(numEntries / ENV.ENTRIES_PER_PAGE);
  })

});

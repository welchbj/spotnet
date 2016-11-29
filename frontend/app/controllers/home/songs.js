import Ember from 'ember';

export default Ember.Controller.extend({

  queryParams: ['page'],

  /**
   * Query param to indicate current page in Spotify's API.
   */
  page: 1,

  /**
   * Static value set to 10.
   */
  entriesPerPage: 10,

  /**
   * The total number of pages available for querying.
   */
  numPages: Ember.computed('model', 'entriesPerPage', function() {
    const numEntries = this.get('model').total;
    const entriesPerPage = this.get('entriesPerPage');
    return Math.ceil(numEntries / entriesPerPage);
  })

});

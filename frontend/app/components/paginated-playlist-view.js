import Ember from 'ember';

export default Ember.Component.extend({

  /**
   * The current page of playlists to view.
   */
  page: null,

  /**
   * The total number of pages.
   */
  numPages: null,

  /**
   * List of playlist objects, returned from Spotify's Web API.
   */
  playlists: null,

  actions: {

    /**
     * Increment the page number, if it is within the allowed bounds.
     */
    incPage() {
      const page = this.get('page');
      if (page < this.get('numPages')) {
        this.set('page', page + 1);
      }
    },

    /**
     * Decrement the page number, if it is within the allowed bounds.
     */
    decPage() {
      const page = this.get('page');
      if (page > 1) {
        this.set('page', page - 1);
      }
    }

  }

});

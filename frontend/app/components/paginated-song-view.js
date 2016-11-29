import Ember from 'ember';

export default Ember.Component.extend({

  /**
   * The current page number.
   */
  page: null,

  /**
   * The total numebr of pages.
   */
  numPages: null,

  /**
   * The array of song objects to be rendered in the paginated view.
   */
  songs: null,

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

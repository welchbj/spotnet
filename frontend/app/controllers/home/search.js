import Ember from 'ember';
import ENV from '../../config/environment';

export default Ember.Controller.extend({

  queryParams: ['q', 'page'],

  q: '',

  page: 1,

  isSearching: false,

  /**
   * Observer to reset the page back to 1 when the query changes.
   */
  qDidChange: Ember.observer('q', function() {
    this.set('page', 1);
  }),

  qIsEmpty: Ember.computed('q', function() {
    return this.get('q') === '';
  }),

  noMatchingTracks: Ember.computed('model.length', function() {
    return this.get('model.length') === 0;
  }),

  numPages: Ember.computed('model', function() {
    const model = this.get('model');
    if (model === null) {
      return null;
    }
    else {
      const numTracks = model.meta.numTracks;
      return Math.ceil(numTracks / ENV.NUM_SONGS_PER_PAGE);
    }
  })

});

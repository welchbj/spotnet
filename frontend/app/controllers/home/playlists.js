import Ember from 'ember';
import ENV from '../../config/environment';

export default Ember.Controller.extend({

  queryParams: ['page'],

  /**
   * The current page with respect to the Spotify Web API's provided
   * access to the user's playlist.
   */
  page: 1,

  numPages: Ember.computed('model', function() {
    const numEntries = this.get('model').total;
    return Math.ceil(numEntries / ENV.NUM_PLAYLISTS_PER_PAGE);
  })

});

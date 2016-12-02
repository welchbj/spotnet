import Ember from 'ember';

export default Ember.Component.extend({

  classNames: ['item'],

  /**
   * A slave object from the spotnet service's `slaves` array.
   */
  slave: null

});

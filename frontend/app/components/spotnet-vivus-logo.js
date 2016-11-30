import Ember from 'ember';
import Vivus from 'vivus';

export default Ember.Component.extend({

  didRender() {
    this._super(...arguments);

    new Vivus('spotnet-logo-vivus-div', {
      file: 'assets/spotnet-logo.svg',
      type: 'scenario'
    });
  }

});

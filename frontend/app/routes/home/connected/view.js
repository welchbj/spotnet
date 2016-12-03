import Ember from 'ember';

export default Ember.Route.extend({

  model(params) {
    // just return slave uuid as the field
    return params.slave_node_id;
  }

});

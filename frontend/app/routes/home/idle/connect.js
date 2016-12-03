import Ember from 'ember';

export default Ember.Route.extend({

  model(params) {
    // just return the slave id as the model
    return params.slave_node_id;
  }

});

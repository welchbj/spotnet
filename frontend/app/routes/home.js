import Ember from 'ember';
import AuthenticatedRouteMixin from '../mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

  spotify: Ember.inject.service(),

  /**
   * Get the user's information.
   */
  model() {
    return this.get('spotify').getMe();
  }

});

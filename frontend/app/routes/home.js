import Ember from 'ember';
import AuthenticatedRouteMixin from '../mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {

  spotify: Ember.inject.service(),

  /**
   * Get the user's information.
   */
  model() {
    return this.get('store').findRecord('user', 'dummy string');
  },

  /**
   * Redirect to home/songs nested route if the home route is accessed
   * directly, so that we are always in one of the tabs of the control panel.
   */
  afterModel(model, transition) {
    if (transition.targetName === 'home.index') {
      this.transitionTo('home.songs');
    }
  }

});

import Ember from 'ember';

export default Ember.Route.extend({

  spotify: Ember.inject.service(),

  model(params) {
    const { error } = params;
    if (error === null) {
      // this is ugly but necessary since Spotify redirects with a hash
      // instead of regular query parameters on successful authentication
      const hashString = window.location.hash;
      const tokenMatches = hashString.match(/access_token=([^&]*)/);
      if (tokenMatches === null) {
        // no matches; someone is requesting a bad URL
        this.transitionTo('index');
      } else {
        const token = tokenMatches[1];
        this.get('spotify').setToken(token);
        this.transitionTo('home');
      }
    } else {
      // authentication failed
      this.transitionTo('index');
    }
  }

});

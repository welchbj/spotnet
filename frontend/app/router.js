import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('auth');
  this.route('home', function() {
    this.route('songs');
    this.route('playlists');
    this.route('connected');
    this.route('idle', function() {
      this.route('connect', { path: '/connect/:slave_node_id' });
    });
    this.route('playlist', { path: '/playlist/:owner_id/:playlist_id' });
    this.route('search');
  });
  this.route('disconnect');
});

export default Router;

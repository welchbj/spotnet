import Ember from 'ember';
import config from '../config/environment';

export default Ember.Controller.extend({

  queryParams: ['msgId'],

  msgId: null,

  MSG_MAPPING: {
    NEED_TO_CONNECT_ACCOUNT: {
      content: 'Whoops! You need to connect your Spotify account before ' +
               'entering the Spotnet app.',
      type: 'warning'
    },
    DISCONNECTED_ACCOUNT: {
      content: 'Your account has been successfully disconnected.',
      type: 'success'
    },
    ERROR_NETWORK_REQUEST: {
      content: 'Something went wrong contacting Spotify\'s API. ' +
               'Perhaps you could try re-connecting your account.',
      type: 'error'
    },
    SPOTNET_MASTER_CONNECTION_FAILED: {
      content: 'Something went wrong when communicating with the Spotnet ' +
               'master server.',
      type: 'error'
    }
  },

  /**
   * The message to be displayed to the user.
   */
  msg: Ember.computed('msgId', function() {
    const MSG_MAPPING = this.get('MSG_MAPPING');
    const msgId = this.get('msgId');

    if (msgId == null || !(msgId in MSG_MAPPING)) {
      this.set('msgId', null);
      return null;
    }

    return MSG_MAPPING[msgId].content;
  }),

  msgColor: Ember.computed('msgId', function() {
    const MSG_MAPPING = this.get('MSG_MAPPING');
    const msgId = this.get('msgId');

    if (msgId == null || !(msgId in MSG_MAPPING)) {
      this.set('msgId', null);
      return null;
    }

    return MSG_MAPPING[msgId].type;
  }),

  spotifyAuthRequestUrl: (
    config.SPOTIFY_AUTH_BASE_URL +
    '?client_id=' +
    config.SPOTIFY_CLIENT_ID +
    '&response_type=token' +
    '&redirect_uri=' +
    encodeURIComponent(config.SPOTIFY_AUTH_REDIRECT_URL) +
    '&scope=' +
    encodeURIComponent(config.SPOTIFY_SCOPE))

});

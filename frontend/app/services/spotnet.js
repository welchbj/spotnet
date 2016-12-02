import Ember from 'ember';
import ENV from '../config/environment';

/**
 * Service for interacting via a WebSocket with the Spotnet master server.
 */
export default Ember.Service.extend({

  /**
   * The WebSocket used to communicate with the master server.
   */
  socketRef: null,

  init() {
    this._super(...arguments);

    this.initSocket();
    this.loadSystemState();
  },

  /**
   * Initialize the socket connection.
   */
  initSocket() {
    console.log(ENV.SPOTNET_MASTER_SERVER_URL);
    const _this = this;

    const socket = new WebSocket(ENV.SPOTNET_MASTER_SERVER_URL);
    socket.onopen = (event) => _this.onSocketOpen(event);
    socket.onmessage = (event) => _this.onSocketMessage(event);
    socket.onclose = (event) => _this.onSocketClose(event);

    this.set('socketRef', socket);
  },

  onSocketOpen(event) {
    // TODO
  },

  onSocketMessage(event) {
    // TODO
  },

  onSocketClose(event) {
    // TODO

    this.set('socketRef', null);
  },

  loadSystemState() {
    // TODO
  }

});

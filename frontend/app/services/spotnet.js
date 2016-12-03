import Ember from 'ember';
import ENV from '../config/environment';

/**
 * Service for interacting via a WebSocket with the Spotnet master server.
 */
export default Ember.Service.extend({

  store: Ember.inject.service(),

  /**
   * The WebSocket used to communicate with the master server.
   */
  socketRef: null,

  /**
   * Configuration property, a Boolean flag indicating whether or not voting
   * to skip a track is enabled.
   */
  votingEnabled: null,

  /**
   * Configuration property, an integer indicating the number of votes
   * required to skip a track.
   */
  votesForSkip: null,

  /**
   * An array of objects representing slave nodes, of the form:
   * {
   *   "uuid": string,
   *   "countedVotesForSkip": number,
   *   "isConnected": boolean,
   *   "name": string,
   *   "firstConnectedAt": isoformat string,
   *   "trackQueue": [{id: 'some id', uri: 'some uri'}, ...]
   * }
   */
  slaves: [],

  /**
   * Boolean flag indicating whether the spotnet service is loading its
   * state from the master server.
   */
  isLoading: true,

  /**
   * Computed property to get array of idle slave objects.
   */
  idleSlaves: Ember.computed('slaves.[]', function() {
    return this.get('slaves').filter((slave) => !slave.isConnected);
  }),

  /**
   * Computed property to get array of connected slave objects.
   */
  connectedSlaves: Ember.computed('slaves.[]', function() {
    return this.get('slaves').filter((slave) => slave.isConnected);
  }),

  /**
   * Boolean flag indicating that there was a connection error when
   * using (or attempting to use) the WebSocket connection with the master
   * server.
   */
  wasConnectionError: false,

  init() {
    this._super(...arguments);

    this.initSocket();
  },

  /**
   * Initialize the socket connection.
   */
  initSocket() {
    const _this = this;

    const socket = new WebSocket(ENV.SPOTNET_MASTER_SERVER_URL);

    socket.onopen = (event) => _this.onSocketOpen(event);
    socket.onmessage = (event) => _this.onSocketMessage(event);
    socket.onclose = (event) => _this.onSocketClose(event);
    socket.onerror = (event) => _this.onSocketError(event);

    this.set('socketRef', socket);
  },

  /**
   * WebSocket open event handler. Requests all system state from the master
   * server.
   */
  onSocketOpen(event) {
    this.requestState();
  },

  /**
   * WebSocket message event handler.
   */
  onSocketMessage(event) {
    const resp = this.getResponse(event);
    const { status, sender, data } = resp;

    if (sender !== 'master') {
      Ember.Logger.log('Invaid sender received on WebSocket connection.');
      return;
    }

    switch (status) {
      case 'send-state':
        this.loadState(data);
        break;
      default:
        Ember.Logger.log('Received invalid status on master server ' +
                         'WebSocket connection.');
    }
  },

  /**
   * WebSocket close event handler.
   */
  onSocketClose(event) {
    Ember.Logger.log('Master server WebSocket closed.');

    this.set('wasConnectionError', true);
    this.set('socketRef', null);
  },

  onSocketError(error) {
    Ember.Logger.log('Error in WebSocket connection:');
    Ember.Logger.log(error);
    this.set('wasConnectionError', true);
  },

  /**
   * Send a JSON object over this service's WebSocket connection. Expects
   * socketRef to be properly initialized and non-null.
   */
  wsSend(jsonObj) {
    this.get('socketRef').send(JSON.stringify(jsonObj));
  },

  /**
   * Parses the Spotnet response object from its position in a WebSocket event
   * object.
   */
  getResponse(event) {
    const { data } = event;
    return JSON.parse(data);
  },

  /**
   * Request all system state from the master server.
   */
  requestState() {
    this.set('isLoading', true);
    this.wsSend({
      status: 'request-state',
      sender: 'web-client'
    });
  },

  /**
   * Load the entire system state from a Spotnet data object sent from the
   * master server.
   */
  loadState(data) {
    // load config properties
    this.setProperties({
      votingEnabled: data['voting-enabled'],
      votesForSkip: data['votes-for-skip']
    });

    // load slave models from the data
    const { slaves } = data;
    this.set('slaves', slaves.map((slaveObj) => {
      return {
        uuid: slaveObj.uuid,
        countedVotesForSkip: slaveObj['counted-votes-for-skip'],
        isConnected: slaveObj['is-connected'],
        name: slaveObj.name,
        firstConnectedAt: slaveObj['first-connected-at'],
        trackQueue: slaveObj['track-queue']
      };
    }));

    this.set('isLoading', false);
  },

  /**
   * Send the credentials for a slave to the master server.
   */
  sendCredentials(uuid, name, username, password) {
    this.wsSend({
      status: 'send-credentials',
      sender: 'web-client',
      data: {
        uuid: uuid,
        name: name,
        username: username,
        password: password
      }
    });

    const slave = this.get('slaves').findBy('uuid', uuid);
    Ember.set(slave, 'isConnected', true);
    Ember.set(slave, 'name', name);
  }

});

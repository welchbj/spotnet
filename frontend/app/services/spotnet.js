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
   *   "loginStatus": string, one of {'idle', 'failed', 'loading'},
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
  idleSlaves: Ember.computed('slaves.@each.isConnected', function() {
    return this.get('slaves').filter((slave) => {
      return !Ember.get(slave, 'isConnected');
    });
  }),

  /**
   * Computed property to get array of connected slave objects.
   */
  connectedSlaves: Ember.computed('slaves.@each.isConnected', function() {
    return this.get('slaves').filter((slave) => {
      return Ember.get(slave, 'isConnected');
    });
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
    console.log(resp);
    const { status, sender, data } = resp;
    let slave;

    if (sender !== 'master') {
      Ember.Logger.log('Invalid sender received on WebSocket connection.');
      return;
    }

    switch (status) {
      case 'send-state':
        this.loadState(data);
        break;
      case 'send-slave-state':
        this.loadSlave(data.slave);
        break;
      case 'add-slave':
        this.addSlave(data.slave);
        break;
      case 'remove-slave':
        this.removeSlave(data.uuid);
        break;
      case 'login-passed':
        slave = this.get('slaves').findBy('uuid', data.uuid);
        Ember.set(slave, 'loginStatus', 'idle');
        Ember.set(slave, 'isConnected', true);
        Ember.Logger.log('Login passed!');
        break;
      case 'login-failed':
        slave = this.get('slaves').findBy('uuid', data.uuid);
        Ember.set(slave, 'loginStatus', 'failed');
        Ember.set(slave, 'isConnected', false);
        Ember.Logger.log('Login failed!');
        break
      default:
        Ember.Logger.log('Received invalid status on master server ' +
                         'WebSocket connection.');

      this.get('slaves').forEach((slave) => console.log(slave));
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
    this.set('slaves', slaves.map(this.normalizeSlaveObj));

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
    Ember.set(slave, 'loginStatus', 'loading');
  },

  /**
   * Remove a slave from the `slaves` attribute by its uuid.
   */
  removeSlave(uuid) {
    const slaves = this.get('slaves');
    this.set('slaves', slaves.filter((slave) => {
      return Ember.get(slave, 'uuid') !== uuid;
    }));
  },

  /**
   * Add a slave to the `slaves` attribute.
   */
  addSlave(slaveObj) {
    this.get('slaves').addObject(this.normalizeSlaveObj(slaveObj));
  },

  /**
   * Update / load a slave into the array of slaves.
   */
  loadSlave(slaveObj) {
    const slave = this.normalizeSlaveObj(slaveObj);
    const { uuid } = slave;
    const toUpdate = this.get('slaves').findBy('uuid', uuid);

    Ember.set(toUpdate, 'countedVotesForSkip', slave.countedVotesForSkip);
    Ember.set(toUpdate, 'isConnected', slave.isConnected);
    Ember.set(toUpdate, 'isPaused', slave.isPaused);
    Ember.set(toUpdate, 'name', slave.name);
    Ember.set(toUpdate, 'firstConnectedAt', slave.firstConnectedAt);
    Ember.set(toUpdate, 'trackQueue', slave.trackQueue);
  },

  /**
   * Add a track to the slave with the specified uuid, at the specified
   * position ('next' or 'current') in its queue. Note that the track argument
   * is a track model.
   */
  sendAddTrack(slaveUuid, position, track) {
    this.wsSend({
      status: 'add-track',
      sender: 'web-client',
      data: {
        uuid: slaveUuid,
        position: position,
        track: {
          id: track.get('id'),
          uri: track.get('spotifyUri')
        }
      }
    });
  },

  /**
   * Remove a track from the slave with the specified uuid, at the specified
   * position.
   */
  sendRemoveTrack(slaveUuid, position) {
    this.wsSend({
      status: 'remove-track',
      sender: 'web-client',
      data: {
        uuid: slaveUuid,
        position: position
      }
    });
  },

  sendPlayAudio(uuid) {
    this.wsSend({
      status: 'play-audio',
      sender: 'web-client',
      data: {
        uuid: uuid
      }
    });
  },

  sendPauseAudio(uuid) {
    this.wsSend({
      status: 'pause-audio',
      sender: 'web-client',
      data: {
        uuid: uuid
      }
    });
  },

  /**
   * Normalize a raw slave object sent from the master server.
   */
  normalizeSlaveObj(slaveObj) {
    return {
        uuid: slaveObj.uuid,
        countedVotesForSkip: slaveObj['counted-votes-for-skip'],
        isConnected: slaveObj['is-connected'],
        loginStatus: 'idle',
        isPaused: slaveObj['is-paused'],
        name: slaveObj.name,
        firstConnectedAt: slaveObj['first-connected-at'],
        trackQueue: slaveObj['track-queue']
      };
  }

});

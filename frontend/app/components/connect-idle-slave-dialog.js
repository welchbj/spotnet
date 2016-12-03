import Ember from 'ember';

export default Ember.Component.extend({

  classNames: ['ui', 'segment'],

  spotnet: Ember.inject.service(),

  /**
   * The user's desired name for the connected node.
   */
  name: null,

  /**
   * The user's Spotify username, to be sent to the master server and
   * propagated to the appropriate slave.
   */
  username: null,

  /**
   * The user's Spotify password, to be sent to the master server and
   * propagated to the appropriate slave.
   */
  password: null,

  /**
   * The error message to display if something goes wrong.
   */
  errMsg: null,

  /**
   * A slave object from the spotnet service's `slaves` array.
   */
  slave: null,

  actions: {

    /**
     * Send credentials to the master to propagate to the appropriate slave.
     */
    sendCredentials() {
      const name = this.get('name');
      const username = this.get('username');
      const password = this.get('password');

      if (!name || !username || !password) {
        this.set('errMsg', 'You must enter all fields.');
        return;
      }

      const uuid = this.get('slave').uuid;

      this.get('spotnet').sendCredentials(uuid, name, username, password);
    },

    /**
     * Reset all of the inputs.
     */
    reset() {
      this.setProperties({
        name: null,
        username: null,
        password: null,
        errMsg: null
      });
    }

  }

});

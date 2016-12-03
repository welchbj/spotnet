import Ember from 'ember';

export default Ember.Component.extend({

  classNames: ['item'],

  spotnet: Ember.inject.service(),

  /**
   * Array of selected slave UUIDs for which to add the song, modified by the
   * modal's dropdown.
   */
  selectedSlaves: null,

  /**
   * A track model representing a Spotify song/track, derived from the Spotify
   * Web API.
   */
  song: null,

  setAsCurrentTrack: true,

  setAsNextTrack: false,

  connectedSlavesDidChange: Ember.observer('spotnet.connectedSlaves', function() {
    const connectedSlaves = this.get('spotnet.connectedSlaves');
    const selectedSlaves = this.get('selectedSlaves');

    if (!selectedSlaves) {
      return;
    }

    // if the Spotnet service's connected slaves changed, one of our selected
    // slaves could no longer be valid
    this.set('selectedSlaves', selectedSlaves.filter((slaveUuid) => {
      return connectedSlaves.findBy('uuid', slaveUuid);
    }));
  }),

  onModalApprove() {
    const selectedSlaves = this.get('selectedSlaves');
    if (selectedSlaves) {
      const spotnet = this.get('spotnet');
      const song = this.get('song');
      const setAsNextTrack = this.get('setAsNextTrack');
      const position = setAsNextTrack ? 'next' : 'current';

      selectedSlaves.forEach((slaveUuid) => {
        spotnet.sendAddTrack(slaveUuid, position, song);
      });
    }

    return true;
  },

  onModalDeny() {
    this.set('selectedSlaves', null);
    return true;
  },

  actions: {

    openModal() {
      if (!this.get('song.isSpotifyTrack')) {
        return;
      }

      const _this = this;
      this.$('.ui.modal')
        .modal({
          detachable: false,
          duration: 100,
          observeChanges: true,
          closable: false,
          onApprove: () => _this.onModalApprove(),
          onDeny: () => _this.onModalDeny()
        })
        .modal('show');
    },

    setAsCurrentTrack() {
      this.setProperties({
        setAsCurrentTrack: true,
        setAsNextTrack: false
      });
    },

    setAsNextTrack() {
      this.setProperties({
        setAsCurrentTrack: false,
        setAsNextTrack: true
      });
    }

  }

});

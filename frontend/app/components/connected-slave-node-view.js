import Ember from 'ember';

export default Ember.Component.extend({

  spotnet: Ember.inject.service(),

  store: Ember.inject.service(),

  /**
   * A slave object from the the spotnet services' `slaves` attribute.
   */
  slave: null,

  isLoadingTracks: false,

  loadedTracks: null,

  currentTrack: Ember.computed('loadedTracks', function() {
    const loadedTracks = this.get('loadedTracks');
    return loadedTracks ? loadedTracks.objectAt(0) : null;
  }),

  comingUpTracks: Ember.computed('loadedTracks', function() {
    const loadedTracks = this.get('loadedTracks');
    if (loadedTracks.get('length') < 1) {
      return null;
    }

    return loadedTracks.slice(1);
  }),

  init() {
    this._super(...arguments);

    this.loadTrackData();
  },

  didRender() {
    this._super(...arguments);
    this.initDimmers();
  },

  trackQueueDidChange: Ember.observer('slave.trackQueue.[]', function() {
    this.loadTrackData();
  }),

  /**
   * Re-initialize dimmers when the list of upcoming tracks changes.
   */
  comingUpTracksDidChange: Ember.observer('comingUpTracks', function() {
    this.initDimmers();
  }),

  initDimmers() {
    this.$('.remove-dimmer').dimmer({
      on: 'hover',
      opacity: 0.55,
      duration: {
        show: 200,
        hide: 200
      }
    });
  },

  loadTrackData() {
    const trackQueue = this.get('slave.trackQueue');
    if (!(trackQueue.length)) {
      this.set('loadedTracks', null);
      return;
    }

    this.set('isLoadingTracks', true);

    this.get('store').query('track', {
      tracksFrom: 'ids',
      ids: trackQueue.mapBy('id').join(',')
    }).then((tracks) => {
      this.setProperties({
        loadedTracks: tracks,
        isLoadingTracks: false
      });
    });
  },

  actions: {

    playCurrentTrack() {

      console.log('Set playing called.')
      // TODO
    },

    pauseCurrentTrack() {

      console.log('Set paused called');
      // TODO
    },

    skipCurrentTrack() {
      const comingUpTracks = this.get('comingUpTracks');
      if (!comingUpTracks) {
        return;
      }

      console.log('Skip called.');
      // TODO
    },

    /**
     * Remove the track. Note that the `trackIndex` argument is the position
     * of the track to remove in the `comingUpTracks` array, so we must
     * increment it by 1 to properly remove the track from the slave's
     * `trackQueue` attribute.
     */
    removeTrack(trackIndex) {
      // TODO
      console.log('Remove track called: ' + trackIndex);
    }

  }

});

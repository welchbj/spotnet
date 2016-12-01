import DS from 'ember-data';

export default DS.JSONAPISerializer.extend({

  /**
   * Normalize a track object returned from Spotify's Web API.
   */
  normalizeTrackObject(track) {
    let normalizedTrack = {
      type: 'track',

      id: track.id,

      attributes: {

        artists: track.artists.getEach('name').join(', '),
        albumName: track.album.name,
        albumImageUrl: track.album.images.length > 0 ? track.album.images[0].url : null,
        durationMs: track.duration_ms,
        spotifyUrl: track.external_urls.spotify,
        name: track.name,
        spotifyUri: track.uri

      }
    };

    if (!normalizedTrack.id) {
      normalizedTrack.id = track.uri;
    }

    return normalizedTrack;
  },

  normalizeQueryResponse(store, primaryModelClass, payload, id, requestType) {  // jshint ignore:line
    let normalizedTracks;
    let numTracks;
    if ('items' in payload) {
      normalizedTracks = payload.items.map((item) => {
        return this.normalizeTrackObject(item.track);
      });
      numTracks = payload.total;
    }
    else {
      normalizedTracks = payload.tracks.items.map((track) => {
        return this.normalizeTrackObject(track);
      });
      numTracks = payload.tracks.total;
    }

    return {
      data: normalizedTracks,
      meta: {
        numTracks: numTracks
      }
    };
  }

});

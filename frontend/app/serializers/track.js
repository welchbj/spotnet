import DS from 'ember-data';

export default DS.JSONAPISerializer.extend({

  /**
   * Normalize a track object returned from Spotify's Web API.
   */
  normalizeTrackObject(track) {
    return {
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
  },

  normalizeQueryResponse(store, primaryModelClass, payload, id, requestType) {
    const numTracks = payload.total;
    let tracks = payload.items.map((item) => this.normalizeTrackObject(item.track));
    return {
      data: tracks,
      meta: {
        numTracks: numTracks
      }
    };
  }

});

import DS from 'ember-data';

export default DS.JSONAPISerializer.extend({

  normalizePlaylistObject(playlist) {
    return {
      type: 'playlist',

      id: playlist.id,

      attributes: {

        description: ('description' in playlist) ? playlist.description : null,
        spotifyUrl: playlist.external_urls.spotify,
        numFollowers: ('followers' in playlist) ? playlist.followers.total : null,
        numTracks: ('tracks' in playlist) ? playlist.tracks.total : null,
        imageUrl: playlist.images.length > 0 ? playlist.images[0].url : null,
        name: playlist.name,
        ownerId: playlist.owner.id,
        spotifyUri: playlist.uri

      }
    };
  },

  normalizeQueryResponse(store, primaryModelClass, payload, id, requestType) {  // jshint ignore:line
    const numPlaylists = payload.total;
    let playlists = payload.items.map((item) => this.normalizePlaylistObject(item));
    return {
      data: playlists,
      meta: {
        numPlaylists: numPlaylists
      }
    };
  },

  normalizeFindRecordResponse(store, primaryModelClass, payload, id, requestType) {  // jshint ignore:line
    return {
      data: this.normalizePlaylistObject(payload)
    };
  }

});

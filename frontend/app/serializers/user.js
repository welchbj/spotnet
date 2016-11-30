import DS from 'ember-data';

export default DS.JSONAPISerializer.extend({

  /**
   * Normalize the response from the Spotify Web API's /me endpoint.
   */
  normalizeFindRecordResponse(store, primaryModelClass, payload, id, requestType) {
    const baseUrl = store.adapterFor('application').get('baseUrl');

    return {
      data: {

        type: 'user',

        id: payload.id,

        attributes: {

          displayName: payload.display_name,
          birthdate: payload.birthdate,
          email: payload.email,
          spotifyUrl: payload.external_urls.spotify,
          numFollowers: payload.followers.total,
          imageUrl: (payload.images.length > 0) ? payload.images[0].url : null,
          hasPremium: payload.product === 'premium',
          spotifyUri: payload.uri

        },

        relationships: {

          savedTracks: {
            links: {
              related: `${baseUrl}/me/tracks`
            }
          },

          playlists: {
            links: {
              related: '${baseUrl}/me/playlists'
            }
          }

        }
      }
    };
  }

});

import ApplicationAdapter from './application';
import Ember from 'ember';

export default ApplicationAdapter.extend({

  urlForQuery(query, modelName) {  // jshint ignore:line
    let url = this.get('baseUrl');

    if (query.tracksFrom === 'me') {
      url += '/me/tracks?';
    }
    else if (query.tracksFrom === 'playlist') {
      const  { ownerId, playlistId } = query;
      url += `/users/${ownerId}/playlists/${playlistId}/tracks?`;
    }
    else if (query.tracksFrom === 'search') {
      const { q } = query;
      url += `/search?q=${q}&type=track&`;
    }
    else if (query.tracksFrom === 'ids') {
      const { ids } = query;
      url += `/tracks?ids=${ids}&`
    }
    else {
      Ember.Logger.log('Unexpected tracksFrom key: ' + query.tracksFrom);
    }

    const { offset, limit } = query;
    if (offset && limit) {
      url += `offset=${offset}&limit=${limit}`;
    }

    return url;
  }

});

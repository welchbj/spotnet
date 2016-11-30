import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({

  urlForQuery(query, modelName) {
    const baseUrl = this.get('baseUrl');
    let url;

    if (query.tracksFrom === 'me') {
      url = `${baseUrl}/me/tracks`;
    }
    else {
      // TODO: handle tracks from playlists
    }

    url += `?offset=${query.offset}&limit=${query.limit}`;
    return url;
  }

});

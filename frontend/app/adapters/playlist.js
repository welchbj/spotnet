import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({

  urlForQuery(query, modelName) {
    const baseUrl = this.get('baseUrl');
    const params = `offset=${query.offset}&limit=${query.limit}`

    return `${baseUrl}/me/playlists?${params}`;
  }

});

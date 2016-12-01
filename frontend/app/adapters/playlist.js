import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({

  urlForQuery(query, modelName) {
    const baseUrl = this.get('baseUrl');
    const params = `offset=${query.offset}&limit=${query.limit}`;

    return `${baseUrl}/me/playlists?${params}`;
  },

  urlForFindRecord(id, modelName, snapshot) {
    const baseUrl = this.get('baseUrl');
    const { ownerId } = snapshot.adapterOptions;
    const params = 'fields=description,external_urls,followers,id,images,name,owner,uri';

    return `${baseUrl}/users/${ownerId}/playlists/${id}/?${params}`;
  }

});

import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({

  /**
   * Access the Spotify Web API endpoint for logged in user info.
   */
  urlForFindRecord(id, modelName, snapshot) {
    const baseUrl = this.get('baseUrl');
    return `${baseUrl}/me`;
  }

});

import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({

  /**
   * Access the Spotify Web API endpoint for logged in user info.
   */
  urlForFindRecord(id, modelName, snapshot) {  // jshint ignore:line
    const baseUrl = this.get('baseUrl');
    return `${baseUrl}/me`;
  }

});

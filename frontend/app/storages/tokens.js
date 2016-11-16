import StorageObject from 'ember-local-storage/local/object';

/**
 * Class for storing access tokens in local storage.
 */
const Storage = StorageObject.extend();

Storage.reopenClass({

  /**
   * Default spotifyToken to null, indicating that
   * this client is not authenticated.
   */
  initialState() {
    return { spotifyAccessToken: null };
  }

});

export default Storage;

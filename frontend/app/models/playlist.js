import attr from 'ember-data/attr';
import Model from 'ember-data/model';
import { hasMany } from 'ember-data/relationships';

/**
 * A Spotify playlist model, derived from Spotify's Web API. See:
 * https://developer.spotify.com/web-api/get-playlist/
 */
export default Model.extend({

  description: attr('string'),

  spotifyUrl: attr('string'),

  numFollowers: attr('number'),

  imageUrl: attr('string'),

  name: attr('string'),

  ownerId: attr('string'),

  spotifyUri: attr('string'),

});

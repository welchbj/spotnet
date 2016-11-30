import attr from 'ember-data/attr';
import Model from 'ember-data/model';
import { hasMany } from 'ember-data/relationships';

/**
 * A Spotify track model, derived from Spotify's Web API. See:
 * https://developer.spotify.com/web-api/get-track/
 */
export default Model.extend({

  artists: attr('string'),

  albumImageUrl: attr('string'),

  durationMs: attr('number'),

  spotifyUrl: attr('string'),

  name: attr('string'),

  spotifyUri: attr('string')

});

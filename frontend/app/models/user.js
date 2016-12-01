import attr from 'ember-data/attr';
import Model from 'ember-data/model';

/**
 * A user model, derived from Spotify's Web API. See:
 * https://developer.spotify.com/web-api/get-current-users-profile/
 *
 * Note that the user is a singleton model for this application, and
 * only represents the user who has currently connected their account
 * to the host.
 */
export default Model.extend({

  displayName: attr('string'),

  birthdate: attr('date'),

  email: attr('string'),

  spotifyUrl: attr('string'),

  numFollowers: attr('number'),

  imageUrl: attr('string'),

  hasPremium: attr('boolean'),

  spotifyUri: attr('string')

});

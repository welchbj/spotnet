import Ember from 'ember';

/**
 * Return Boolean AND of two arguments.
 */
export function and(params) {
  return params[0] && params[1];
}

export default Ember.Helper.helper(and);

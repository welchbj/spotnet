import Ember from 'ember';

/**
 * Helper to return whether two arguments are equal.
 */
export function eq(params) {
  return params[0] === params[1];
}

export default Ember.Helper.helper(eq);

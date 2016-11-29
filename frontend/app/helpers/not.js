import Ember from 'ember';

/**
 * Returns the Boolean NOT of an argument.
 */
export function not(params) {
  return !(params[0]);
}

export default Ember.Helper.helper(not);

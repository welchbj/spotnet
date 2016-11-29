import Ember from 'ember';

/**
 * Return Boolean OR of two arguments.
 */
export function or(params) {
  return params[0] || params[1];
}

export default Ember.Helper.helper(or);

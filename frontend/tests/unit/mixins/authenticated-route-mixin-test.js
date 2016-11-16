import Ember from 'ember';
import AuthenticatedRouteMixinMixin from 'frontend/mixins/authenticated-route-mixin';
import { module, test } from 'qunit';

module('Unit | Mixin | authenticated route mixin');

// Replace this with your real tests.
test('it works', function(assert) {
  let AuthenticatedRouteMixinObject = Ember.Object.extend(AuthenticatedRouteMixinMixin);
  let subject = AuthenticatedRouteMixinObject.create();
  assert.ok(subject);
});

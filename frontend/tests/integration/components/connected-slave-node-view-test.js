import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('connected-slave-node-view', 'Integration | Component | connected slave node view', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{connected-slave-node-view}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#connected-slave-node-view}}
      template block text
    {{/connected-slave-node-view}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});

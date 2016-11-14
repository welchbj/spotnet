/*jshint node:true*/
/* global require, module */
var EmberApp = require('ember-cli/lib/broccoli/ember-app');

module.exports = function(defaults) {
  var app = new EmberApp(defaults, {
    SemanticUI: {
      import: {
        css: true,
        javascript: true,
        images: true,
        fonts: true
      },

      source: {
        css: 'vendor/semantic/dist',
        javascript: 'vendor/semantic/dist',
        images: 'vendor/semantic/dist/themes/default/assets/images',
        fonts: 'vendor/semantic/dist/themes/default/assets/fonts'
      },

      destination: {
        images: 'assets/themes/default/assets/images',
        fonts: 'assets/themes/default/assets/fonts'
      }
    }
  });

  // Use `app.import` to add additional libraries to the generated
  // output files.
  //
  // If you need to use different assets in different
  // environments, specify an object as the first parameter. That
  // object's keys should be the environment name and the values
  // should be the asset to use in that environment.
  //
  // If the library that you are including contains AMD or ES6
  // modules that you would like to import into your application
  // please specify an object with the list of modules as keys
  // along with the exports of each module as its value.

  return app.toTree();
};

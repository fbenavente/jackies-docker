(function () {
  'use strict';

  angular
    .module('jackies.layout', [
      'jackies.layout.controllers',
      'jackies.layout.directives'
    ]);

  angular
    .module('jackies.layout.controllers', ['ngDialog']);

    angular
    .module('jackies.layout.directives', []);
})();

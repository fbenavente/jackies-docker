(function () {
  'use strict';

  angular
    .module('jackies.management', [
      'jackies.management.controllers',
      'jackies.management.services'
    ]);

  angular
    .module('jackies.management.controllers', []);

  angular
    .module('jackies.management.services', ['ngCookies']);
})();

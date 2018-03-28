(function () {
  'use strict';

  angular
    .module('jackies.interpolate')
    .config(config);

  config.$inject = ['$interpolateProvider'];

  /**
  * @name config
  * @desc We use [[variable]] for angular instead {{variable}} to avoid conflicts with django
  */
  function config($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
  }
})();


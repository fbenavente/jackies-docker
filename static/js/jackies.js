(function () {
  'use strict';

  angular
    .module('jackies', [
          'jackies.routes',
          'jackies.management',
          'jackies.config',
          'jackies.interpolate',
          'jackies.layout',
          'ngCookies'
    ]);

  angular
    .module('jackies.routes', ['ngRoute']);

    angular
  .module('jackies.config', []);

    angular
  .module('jackies.interpolate', []);

    angular
    .module('jackies.management', ['ngDialog']);

    angular
  .module('jackies')
  .run(run);

    run.$inject = ['$http'];

    angular
  .module('jackies').filter('capitalizeWord', function() {
    return function(input, scope) {
        if (input != null && input != undefined)
        {
            input = input.toLowerCase();
            return input.substring(0, 1).toUpperCase() + input.substring(1);
        }
        else{
            return input
        }
      }
    });

    /**
    * @name run
    * @desc Update xsrf $http headers to align with Django's defaults
    */
    function run($http) {
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
    }

})();

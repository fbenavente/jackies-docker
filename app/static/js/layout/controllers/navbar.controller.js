/**
* NavbarController
* @namespace jackies.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('jackies.layout.controllers')
    .controller('NavbarController', NavbarController);

  NavbarController.$inject = ['$scope', 'Authentication'];

  /**
  * @namespace NavbarController
  */
  function NavbarController($scope, Authentication) {
    var vm = this;

    vm.logout = logout;
      $('.nav a').on('click', function(){
    $('.navbar-toggle').click(); //bootstrap 3.x by Richard
});

    /**
    * @name logout
    * @desc Log the user out
    * @memberOf jackies.layout.controllers.NavbarController
    */
    function logout() {
      Authentication.logout();
    }
  }
})();

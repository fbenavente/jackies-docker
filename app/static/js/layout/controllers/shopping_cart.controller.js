/**
* ShoppingCartController
* @namespace jackies.layout.controllers
*/
(function () {
    'use strict';

    angular
    .module('jackies.layout.controllers')
    .controller('ShoppingCartController', ShoppingCartController);

    ShoppingCartController.$inject = ['$scope', 'api', 'generic_functions', '$timeout', '$interval', '$cookies'];

    /**
    * @namespace ShoppingCartController
    */
    function ShoppingCartController($scope, api, generic_functions, $timeout, $interval, $cookies) {

        $scope.products = [];
        $scope.cart_count = 0;

        $scope.emptyCart = function(){
            $scope.products = [];
            $scope.cart_count = 0;
            var cookies = $cookies.getAll();
            angular.forEach(cookies, function (v, k) {
                $cookies.remove(k);
            });
        };

        $scope.$on('addToCart', function(event, product, wedding) {
            var exist = false;
            $scope.cart_count +=1;
            angular.forEach($scope.products, function(prod, index){
                if(prod.product == product && prod.wedding == wedding){
                    prod.qty += 1;
                    exist = true;
                }
            });
            if(!exist){
                $scope.products.push({"qty":1, "product":product, "wedding":wedding});
            }
            $scope.updateProductsCookies();
        });

        $scope.updateProductsCookies = function(){
            // Initialize an object to be saved as the cookie
            var productsCookie = {};
            // Loop through the items in the cart
            angular.forEach($scope.products, function(item) {
                // Add each item to the items cookie,
                // using the product id as the key and the quantity as the value
                    productsCookie[item.product.id] = {"qty":item.qty, "wedding":item.wedding};
            });
            // Use the $cookieStore service to persist the itemsCookie object to the cookie named 'items'
            $cookies.putObject('products', productsCookie);
        };

        $scope.recoverProductsCookies = function(){
            // Initialize the itemsCookie variable
            var productsCookie;
            // Check if cart is empty
            if(!$scope.products.length) {
                // Get the items cookie
                productsCookie = $cookies.getObject('products');
                // Check if the item cookie exists
                if (productsCookie) {
                    // Loop through the items in the cookie
                    angular.forEach(productsCookie, function(data, key) {
                        // Get the product details from the ProductService
                        api.getProduct(key).then(function (response) {
                            var product = {"qty": data["qty"], "product": response.data, "wedding": data["wedding"]};
                            // Add the product to the cart items
                            $scope.products.push(product);
                            $scope.cart_count +=data["qty"];
                        });
                    });
                }
            }

        };

        $scope.recoverProductsCookies();

    }
})();



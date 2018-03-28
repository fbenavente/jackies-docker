// All post, put, get and delete services for jackies management
angular.module('jackies.management.services').factory('api', ['$http', function($http) {
	$http.defaults.headers.post["Content-Type"] = "application/json";

	return {
		getProducts: function() {
			return $http.get('/management/manage_products/').then(function(result) {
				return result;
			})
		},
        getProduct: function(pk) {
			return $http.get('/management/manage_products/'+pk).then(function(result) {
				return result;
			})
		},
        getBackgrounds: function() {
			return $http.get('/management/manage_backgrounds/').then(function(result) {
				return result;
			})
		},
		saveCategory: function(category) {
			return $http.post('/controller_admin/api/manage_categories/', category).then(function(result) {
				return result;
			})
		},
		updateCategory: function(category_id, category) {
			return $http.put('/controller_admin/api/manage_categories/' + category_id, category).then(function(result) {
				return result;
			})
		},
		deleteCategory: function(category_id) {
			return $http.delete('/controller_admin/api/manage_categories/' + category_id).then(function(result) {
				return result;
			})
		}
	}
}]);

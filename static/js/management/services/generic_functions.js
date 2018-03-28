angular.module('jackies.management.services').factory('generic_functions', ['$rootScope', '$q',function($rootScope, $q) {
	return {
			navigate: function(path) {
				window.location.href = path;
			},
			show_message: function (text, success) {
				var alert = $("#alert_message");

				alert.removeClass(success ? "alert-danger": "alert-success");
				alert.addClass(success ? "alert-success" : "alert-danger");

				$("#alert_message_text").html(text);

				alert.show();

				alert.fadeTo(5000, 1000).slideUp(1000, function(){
					$("#alert_message").hide();
				});
			},
			get_error_message: function(response) {
				if(response){
					for(var key in response.data)
						if(response.data.hasOwnProperty(key))
							return response.data[key] + " [" + key + "]";

					if(response.status == 0)
						return gettext("There was an error trying to connect to the selected controller.");
				}
				return gettext("There was an error");
			}
        };
}]);
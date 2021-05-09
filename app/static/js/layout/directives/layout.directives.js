/**
* ImageLoadingDirective
* @namespace jackies.layout.directives
*/
(function () {
    'use strict';

    var app = angular.module('jackies.layout.directives', []);

    app.directive('imageOnload', function() {
        return {
            restrict: 'A',

            link: function(scope, element, attrs) {

                  element.on('load', function() {
                // call the function that was passed
                //scope.$apply(attrs.imageOnload);
                      $("#loading").hide();
                      $("#product-preview").removeClass("dropdown-hidden");

                // usage: <img ng-src="src" image-onload="imgLoadedCallback()" />
            });
            }
        };
    });

    app.directive('modalReposition', function() {
        return {
            restrict: 'A',

            link: function(scope, element, attrs) {

                  element.on('shown.bs.modal', function() {
                        var dialog = $(element).find('.modal-dialog');
                      $(element).css("margin-top", Math.max(0, ($(window).height() - dialog.height()) / 2));
            });
            }
        };
    });


    })();
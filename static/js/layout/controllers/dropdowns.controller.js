/**
* DropdownsController
* @namespace jackies.layout.controllers
*/
(function () {
    'use strict';

    angular
    .module('jackies.layout.controllers')
    .controller('DropdownsController', DropdownsController);

    DropdownsController.$inject = ['$scope', 'api', 'generic_functions', '$timeout', '$interval'];

    /**
    * @namespace DropdownsController
    */
    function DropdownsController($scope, api, generic_functions, $timeout, $interval) {
        var vm = this;
        $scope.image_ratio = 1.5;
        $scope.window_height = 0;
        $scope.image_width = 0;
        $scope.productsDict = {};
        $scope.flavors_per_category = {};
        $scope.sizes_per_flavor_category = {};
        $scope.categories = [];
        $scope.backgrounds = {};
        $scope.currentBackground = 1;
        $scope.categoryQuestionNumber = "1";
        $scope.flavorQuestionNumber = "2";
        $scope.sizeQuestionNumber = "3";
        $scope.selectedDropdownItem = {
            "category": "Que quiero?",
            "flavor": "De que tipo?",
            "size": "Que tamaño?"
        };
        $scope.flavor_number_class = "";
        $scope.size_number_class = "";
        $scope.selectedProduct = "";
        $scope.images = [];
        $scope.wedding_active = false;
        $scope.product_detail_margin = "";
        var myInterval;
        //$scope.pruebas = ["http://s1.1zoom.me/big3/477/356011-sepik.jpg","https://chancano.files.wordpress.com/2013/02/p1030184.jpg", "https://aliciaesclapez.com/wp-content/uploads/2014/01/Caos-C%C3%ADclico-92x73.jpg"];

        // Calculating margin-top for product image and dropdowns vertical center

        $scope.verticalCenter = {
            "image": {"margin-top":"0px"},
            "category":{},
            "flavor": {},
            "size": {}
        };

        $scope.setDropdownsCenters = function(){
            var navbar_height = $(".navbar").height();
            var navbar_margin = parseInt($(".navbar").css("margin-bottom"));
            var dropdown_category_height = $("#dropdown-category").height();
            var margin_top_category = ($(window).height()/2) - (dropdown_category_height/2) - navbar_height - navbar_margin;
            var margin_top_dropdowns = margin_top_category - (dropdown_category_height/2);
            $scope.verticalCenter["category"] = {"margin-top": parseInt(margin_top_category) + "px"};
            $scope.verticalCenter["flavor"] = {"margin-top": parseInt(margin_top_dropdowns) + "px"};
            $scope.verticalCenter["size"] = {"margin-top": parseInt(margin_top_dropdowns) + "px"};
        };


        $scope.setImageMarginTop = function(first){
            $scope.window_height = $(window).height();
            $scope.image_width = $("#product-preview-subcontainer").width();
            var image_container_height = $scope.image_width / $scope.image_ratio;
            //$("#product-preview-subcontainer").height(image_container_height);
            var container_height = $scope.window_height;
            var navbar_margin = parseInt($(".navbar").css("margin-bottom"));
            var navbar_height = $("#jackies_navbar").height();
            var row_category_height = $("#dropdown-category").height();
            if(first){
                row_category_height = row_category_height / 2;
            }
            //var margin_top_temp = (container_height / 2) - (image_height / 2);
            var margin_top = (container_height - navbar_height - navbar_margin - row_category_height - image_container_height)/2;
            if (margin_top < 0) {
                margin_top = 30;
            }
            // we update the margin-top of the product image ONLY if the difference with the previous margin is significant (+-10)
            if((parseInt($scope.verticalCenter["image"]["margin-top"]) < margin_top -10) || (parseInt($scope.verticalCenter["image"]["margin-top"]) > margin_top +10)) {

                // method apply allows to include angular bindings inside jquery functions
                $timeout(function () {
                    $scope.verticalCenter["image"] = {"margin-top": parseInt(margin_top) + "px"};
                },10);
            }

        };


        //Function to select the category, flavor or size
        $scope.selectDropdown = function(btn_name, item_selected){
            $scope.selectedDropdownItem[btn_name] = item_selected;

            $("#dropdown-" + btn_name).removeClass("col-xs-10 col-xs-offset-1 col-sm-8 col-sm-offset-2").addClass("col-xs-4");
            $scope.verticalCenter[btn_name] = {};
            $("#dropdown-" + btn_name + "-btn").removeClass("btn-question-big").addClass("btn-question-small");
            $("#dropdown-" + btn_name + "-menu").removeClass("dropdown-menu-big").addClass("dropdown-menu-small");
            $("#dropdown-" + btn_name + "-btn .question-text").addClass("xs-hidden");
            if (btn_name == "category") {
                if ("" in $scope.productsDict[item_selected]) {
                    $scope.selectedDropdownItem["flavor"] = "";
                    $scope.hideRow("flavor");
                    $scope.flavor_number_class = "";
                    if ("" in $scope.productsDict[item_selected][""]) {
                        $scope.selectedDropdownItem["size"] = "";
                        $scope.hideRow("size");
                        $scope.size_number_class = "";
                        $scope.loadProduct($scope.productsDict[item_selected][""][""]);
                    }
                    else{
                        $scope.closeProduct();
                        if($("#dropdown-size-btn").hasClass("btn-question-small")){
                            $scope.size_number_class = "blink";
                        }
                        $scope.selectedDropdownItem["size"] = "Que tamaño?";
                        $scope.sizeQuestionNumber = "2";
                        $scope.showRow("size");
                    }
                }
                else{
                    $scope.closeProduct();
                    $scope.hideRow("size");
                    if($("#dropdown-flavor-btn").hasClass("btn-question-small")){
                            $scope.flavor_number_class = "blink";
                            $scope.size_number_class = "";
                        }
                    $scope.sizeQuestionNumber = "3";
                    $scope.selectedDropdownItem["flavor"] = "De que tipo?";
                    $scope.showRow("flavor");
                }
            }
            else {
                if (btn_name == "flavor") {
                    $("#dropdown-" + btn_name).addClass("col-xs-offset-4 margin-negative");
                    if ("" in $scope.productsDict[$scope.selectedDropdownItem["category"]][item_selected]) {
                        $scope.selectedDropdownItem["size"] = "";
                        $scope.hideRow("size");
                        $scope.flavor_number_class = "";
                        $scope.loadProduct($scope.productsDict[$scope.selectedDropdownItem["category"]][item_selected][""]);
                    }
                    else{
                        $scope.closeProduct();
                        if($("#dropdown-size-btn").hasClass("btn-question-small")){
                            $scope.size_number_class = "blink";
                            $scope.flavor_number_class = "";
                        }
                        $scope.selectedDropdownItem["size"] = "Que tamaño?";
                        $scope.showRow("size");
                    }

                }
                else {
                    if (btn_name == "size") {
                        $("#dropdown-" + btn_name).addClass("col-xs-offset-8 margin-negative");
                        $scope.loadProduct($scope.productsDict[$scope.selectedDropdownItem["category"]][$scope.selectedDropdownItem["flavor"]][item_selected]);
                        $scope.size_number_class = "";
                    }
                }
            }
        };

        // seteamos los margenes top de los dropdowns e imagen producto para que queden centrados
        $scope.setDropdownsCenters();
        $scope.setImageMarginTop(true);

        // Load backgrounds
        api.getBackgrounds().then(function(response) {
            $scope.backgrounds = response.data;
            var img = new Image();
            img.onload = function() {
                $( 'body' ).css( 'background-image', 'url(' + $scope.backgrounds.results[0].image + ')' );
                $scope.loadAllBackgrounds();
            };
            img.src = $scope.backgrounds.results[0].image;
            $scope.images.push(img);
        },
        function(response) {
            //generic_functions.show_message(generic_functions.get_error_message(response), false);
        });

        $scope.loadAllBackgrounds = function(){

            angular.forEach($scope.backgrounds.results, function(background, index){
                if(index != 0){
                    var img = new Image();
                    if(index == $scope.backgrounds.results.length - 1){
                        img.onload = function() {
                            $scope.backgroundTransitionsInit();
                        };
                    }
                    img.src = $scope.backgrounds.results[index].image;
                    $scope.images.push(img);
                }
            });

        };


        $scope.backgroundTransitionsInit = function(){
            myInterval = $interval(function(){

                $('body').css('background-image', 'url(' + $scope.backgrounds.results[$scope.currentBackground].image + ')');

                if($scope.currentBackground < $scope.backgrounds.count - 1){
                    $scope.currentBackground++;
                }
                else{
                    $scope.currentBackground = 0;
                }
            }, 10000);
        };

        $scope.$on('$destroy', function() {
                $interval.cancel( myInterval );
            });

        // Load products dict
        api.getProducts().then(function(response) {
            $scope.categories = response.data["categories"];
            $scope.flavors_per_category = response.data["flavors"];
            $scope.sizes_per_flavor_category = response.data["sizes"];
            $scope.productsDict = response.data["products"];
            $("#dropdown-category").removeClass("dropdown-hidden");
        },
        function(response) {
            //generic_functions.show_message(generic_functions.get_error_message(response), false);
        });

        $scope.showRow = function(element_name){
            $("#row-"+element_name).show("fast", function () {
                    // Animation complete.
                    $("#dropdown-"+element_name).removeClass("dropdown-hidden");
                });

        };

        $scope.hideRow = function(element_name){
            $("#row-"+element_name).hide("slow", function () {
                    // Animation complete.
                    $("#dropdown-"+element_name).addClass("dropdown-hidden");
                });

        };

        $scope.loadProduct = function(product){
            if($scope.window_height != $(window).height() && $scope.image_width != $("#product-preview-subcontainer").width()){
                $scope.setImageMarginTop(false);
            }

            if($scope.selectedProduct.image != product["image"]) {
                $("#loading").show();
            }
            else{
                $("#loading").hide();
                $("#product-preview").removeClass("dropdown-hidden");
            }

            $scope.selectedProduct = product;
            $("#wrapper").addClass("wrapper-back-modal");
        };

        $scope.closeProduct = function(){
            $("#product-preview").addClass("dropdown-hidden");
            $("#wrapper").removeClass("wrapper-back-modal");
        };

        $scope.showProductDetail = function(){
            $("#product-detail").css("margin-bottom","0px");
        };

        $scope.hideProductDetail = function(){
            $("#product-detail").css("margin-bottom", $scope.product_detail_margin);
        };

        $scope.$watch('selectedProduct', function() {
            $timeout(function () {
                $scope.product_detail_margin = "-"+$("#product-detail").height()+"px";
            },10);
        });

        $scope.add_to_cart = function(wedding){
           $scope.$broadcast ('addToCart', $scope.selectedProduct, wedding);
        };
    }
})();


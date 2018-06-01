function removeOptions(selectbox)
{
    if (selectbox === null){
        return;
    }
    var i;
    for(i = selectbox.options.length - 1 ; i >= 0 ; i--)
    {
        selectbox.remove(i);
    }
}

function setProductValuesFor(productFamily, flavor, size, sugar_free_data, data_as_json){
    var flavorSelectId = productFamily + "_flavors";
    var sizeSelectId = productFamily + "_sizes";

    if (flavor == ''){
        var flavorSelect = document.getElementById(flavorSelectId);
        removeOptions(flavorSelect);
        var opt = document.createElement('option');
        opt.value = '0';
        opt.innerHTML = 'no aplica';
        flavorSelect.appendChild(opt);
    }
    if (size == ''){
        var sizeSelect = document.getElementById(sizeSelectId);
        removeOptions(sizeSelect);
        var opt = document.createElement('option');
        opt.value = '0';
        opt.innerHTML = 'no aplica';
        sizeSelect.appendChild(opt);
    }

    var selectedProduct = null;
    if ($('#sugar_free').is(':checked') && productFamily === 'torta_de_panqueque' ){
        var data = sugar_free_data.price_data;
        selectedProduct = data[flavor][size]; 
    }
    else{
        var data = data_as_json;
        var availableProducts = data.products;
        selectedProduct = availableProducts[productFamily][flavor][size];               
    }

    // set prices
    document.getElementById(productFamily + "_price").innerHTML = "$" + selectedProduct.price;
    document.getElementById(productFamily + "_price_input").value = selectedProduct.price;
    // set product id
    document.getElementById(productFamily + "_product_id").value = selectedProduct.id;
    // set product description
    if ($('#sugar_free').is(':checked') && productFamily === 'torta_de_panqueque' ){
        var data = sugar_free_data.price_data;
        var product = data[flavor][size]; 
        console.log("HERE");
        document.getElementById(productFamily + "_product_desc").value = "(SIN AZÚCAR) " + product.flavor + " | " + product.size;  
    }
    else{
        console.log("ELSE");
        document.getElementById(productFamily + "_product_desc").value = flavor + " | " + size;  
    }  
}

function setSizeOptions(sizeSelect, sizesForFlavor, use_name_as_id){
    var newLength = sizesForFlavor.length;
    // populate with options
    var emptyOpt = document.createElement('option');
    emptyOpt.value = "0";
    emptyOpt.innerHTML = "seleccione tamaño ---";
    sizeSelect.appendChild(emptyOpt);

    for (var i = 0; i<newLength; i++){
        var opt = document.createElement('option');
        if (use_name_as_id){
            opt.value = sizesForFlavor[i].name;
        }else{
            opt.value = sizesForFlavor[i].id;
        }
        opt.innerHTML = sizesForFlavor[i].name;
        sizeSelect.appendChild(opt);
    }
}

function createFlavorSelectListener(productFamily, sugar_free_data, data_as_json){
    var flavorSelectId = productFamily + "_flavors";
    var sizeSelectId = productFamily + "_sizes";

    $("#" + flavorSelectId).change(function () {
        var selectedFlavor = $(this).val();
        var data = data_as_json;
        var availableSizes = data.sizes;
        // get sizes for flavor
        var sizesForFlavor = null;
        var use_name_as_id = true;
        if ($('#sugar_free').is(':checked') && productFamily === 'torta_de_panqueque' ){
            use_name_as_id = false;
            sizesForFlavor = sugar_free_data.sizes;
        }else{
            sizesForFlavor = availableSizes[productFamily][selectedFlavor];
        }
        // clean all options first
        removeOptions(document.getElementById(sizeSelectId));
        var sizeSelect = document.getElementById(sizeSelectId);
        var newLength = sizesForFlavor.length;

        // if no options populate prices instantly
        if (newLength == 1){
            setProductValuesFor(productFamily, selectedFlavor, '', sugar_free_data, data_as_json);
        }
        else{
            setSizeOptions(sizeSelect, sizesForFlavor, use_name_as_id);
            // populate with options
            /*
            var emptyOpt = document.createElement('option');
            emptyOpt.value = "0";
            emptyOpt.innerHTML = "seleccione tamaño ---";
            sizeSelect.appendChild(emptyOpt);

            for (var i = 0; i<newLength; i++){
                var opt = document.createElement('option');
                opt.value = sizesForFlavor[i].name;
                opt.innerHTML = sizesForFlavor[i].name;
                sizeSelect.appendChild(opt);
            }*/
        }
    });
}

function createSizeSelectListener(productFamily, sugar_free_data, data_as_json){
    var flavorSelectId = productFamily + "_flavors";
    var sizeSelectId = productFamily + "_sizes";

    $("#" + sizeSelectId).change(function () {
        var selectedSize = $(this).val();
        var flavors = document.getElementById(flavorSelectId);
        var selectedFlavor = flavors.options[flavors.selectedIndex].value;
        setProductValuesFor(productFamily, selectedFlavor, selectedSize, sugar_free_data, data_as_json);

    });  
}

function isSingleSize(productFamily, data_as_json){
    var data = data_as_json;
    var flavors = data['sizes'][productFamily];
    if (flavors[''] !== undefined){
        return true;
    }
    else{
        return false;
    }
}

function isSingleFlavor(productFamily, data_as_json){
    var data = data_as_json;
    var flavors = data['flavors'][productFamily];
    if (flavors.length > 1){
        return false;
    }
    else{
        return true;
    }
}


function createListeners(product_families, sugar_free_data, data_flavors, data_as_json){
    // special listener
    $("#sugar_free").change(function() {
        if(this.checked) {
            removeOptions(document.getElementById("torta_de_panqueque_flavors"));
            removeOptions(document.getElementById("torta_de_panqueque_sizes"));
            document.getElementById("torta_de_panqueque_price").innerHTML = "" ;
            document.getElementById( "torta_de_panqueque_price_input").value = '';

            var flavor_selector = document.getElementById("torta_de_panqueque_flavors");
            var emptyOpt = document.createElement('option');
            emptyOpt.value = "0";
            emptyOpt.innerHTML = "Seleccione tipo ---";
            flavor_selector.appendChild(emptyOpt);

            var sugar_free_flavors = sugar_free_data.flavors;
            for (var i = 0; i < sugar_free_flavors.length; i++){
                var opt = document.createElement('option');
                opt.value = sugar_free_flavors[i].id;
                opt.innerHTML = sugar_free_flavors[i].name;
                flavor_selector.appendChild(opt);
            }
        }
        else{
            removeOptions(document.getElementById("torta_de_panqueque_flavors"));
            removeOptions(document.getElementById("torta_de_panqueque_sizes"));
            document.getElementById("torta_de_panqueque_price").innerHTML = "" ;
            document.getElementById( "torta_de_panqueque_price_input").value = '';

            var flavor_selector = document.getElementById("torta_de_panqueque_flavors");
            var emptyOpt = document.createElement('option');
            emptyOpt.value = "0";
            emptyOpt.innerHTML = "Seleccione tipo ---";
            flavor_selector.appendChild(emptyOpt);
            var flavors = data_flavors.torta_de_panqueque;
            for (var i = 0; i < flavors.length; i++){
                var opt = document.createElement('option');
                opt.value = flavors[i].normaliz_name;
                opt.innerHTML = flavors[i].name;
                flavor_selector.appendChild(opt);
            }
        }
    });

    var product_families = product_families;
    // create listeners
    for (var i = 0; i<product_families.length; i++){
        // set inmediatly values
        if (isSingleFlavor(product_families[i], data_as_json) === true && isSingleSize(product_families[i], data_as_json) === true){
            setProductValuesFor(product_families[i], '', '', sugar_free_data, data_as_json);
        }

        // conditional if not remove and put price
        if (isSingleFlavor(product_families[i], data_as_json) === true){
            
        }else{
            // available flavors
            createFlavorSelectListener(product_families[i], sugar_free_data, data_as_json); 
        }

        if (isSingleSize(product_families[i], data_as_json) === true){
            
        }else{
            // conditional if not remove and put price
            createSizeSelectListener(product_families[i], sugar_free_data, data_as_json);
        }
    }
}

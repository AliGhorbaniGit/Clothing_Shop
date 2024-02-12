
    function colorChoices(size, color, count) {
        document.getElementById(size).innerHTML = color;
        document.getElementById('qty').max = count;
        document.getElementById('product_color').value = color;
    }

    function sizeChoices(i) {
        document.getElementById('size').innerHTML = i;
        document.getElementById(i).style.display = 'block';
        document.getElementById('product_size').value = i;
    }

    function ChoicesCart(i) {
        document.getElementById(i).style.display = 'block';
    }


    function page_indicator(i) {
        document.getElementById('page').style.backgroundColor = 'red';
    }

    function page_indicator(i) {
        i.style.backgroundColor = 'red'
    }

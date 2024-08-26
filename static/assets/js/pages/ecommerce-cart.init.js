/*
Template Name: Minible - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: ecommerce cart Js File
*/

var defaultOptions = {
};

$('[data-toggle="touchspin"]').each(function (idx, obj) {
    var objOptions = $.extend({}, defaultOptions, $(obj).data());
    $(obj).TouchSpin(objOptions);
});
// function incrementValue() {
//     var inputElement = document.querySelector('input[name="demo_vertical"]');
//     var currentValue = parseInt(inputElement.value);
//     inputElement.value = currentValue + 1;
// }

// function decrementValue() {
//     var inputElement = document.querySelector('input[name="demo_vertical"]');
//     var currentValue = parseInt(inputElement.value);
//     // Ensure the value doesn't go below 0
//     inputElement.value = currentValue > 0 ? currentValue - 1 : 0;
// }


// input spinner value ++ or --

function getDivFromTheElement(element) {
    let temp = element.parentNode.querySelector('input.product-quantity')

    if (!temp) {
        const upperParent = element.parentNode
        return getDivFromTheElement(upperParent)
    }
    return temp
}
// input spin
function inputSpinComponets() {
    isData();

    function isData() {
        const plusElements = document.querySelectorAll('div.plus');
        const minusElements = document.querySelectorAll('div.minus');

        if (plusElements.length) {
            plusElements.forEach(element => {
                element.addEventListener('click', (event) => {
                    const inputElement = getDivFromTheElement(event.target);
                    let inputVal = Number(inputElement.value);
                    const maxVal = Number(inputElement.getAttribute('max'));
                    if (inputVal < maxVal) {
                        inputElement.value = inputVal + 1;
                        updateQuantity(inputElement);
                        remveBtn(inputElement);
                    }
                });
            });
        }

        if (minusElements.length) {
            minusElements.forEach(element => {
                element.addEventListener('click', (event) => {
                    const inputElement = getDivFromTheElement(event.target);
                    let inputVal = Number(inputElement.value);
                    const minVal = Number(inputElement.getAttribute('min'));
                    if (inputVal > minVal) {
                        inputElement.value = inputVal - 1;
                        updateQuantity(inputElement);
                        remveBtn(inputElement);
                    }
                });
            });
        }
    }

    function updateQuantity(quantityInput) {
        var productRow = quantityInput.closest('.product');
        var productList = quantityInput.closest('.product-list');
        var price = parseFloat(productRow.querySelector('.product-price span')?.innerHTML || 0);
        var quantity = parseFloat(quantityInput.value);
        var linePrice = price * quantity;

        Array.from(productRow.getElementsByClassName('product-line-price')).forEach(function (e) {
            e.innerHTML = linePrice.toFixed(2);
            recalculateCart();
        }); 
        
    }
    // Add remove button functionality
    function remveBtn(productElement) {
        var productRow = productElement.closest('.product');
        var removeButton = productRow.querySelector('.remove-button');
        if (removeButton) {
            removeButton.addEventListener('click', function () {
                productRow.remove();
                recalculateCart();
            });
        }
    }

    // recalculate value
    function recalculateCart() {
      var elm = document.querySelector(".product-list")
        var subtotal = 0;
        Array.from(elm.getElementsByClassName("product")).forEach(function (item) {
            Array.from(item.getElementsByClassName('product-line-price')).forEach(function (e) {
                subtotal += parseFloat(e.innerHTML);
            });
        });
        
        var currencySign = "$";
        var taxRate = 0.125;
        var shippingRate = 65.00;
        var discountRate = 0.15;

        /* Calculate totals */
        var tax = subtotal * taxRate;
        var discount = subtotal * discountRate;

        var shipping = (subtotal > 0 ? shippingRate : 0);
        var newTotal = subtotal + tax + shipping - discount;
       
        const cartSubtitle = elm.parentElement.nextElementSibling.querySelector(".totalTable .tTable .cart-subtotal")
        if (cartSubtitle) {
            cartSubtitle.innerHTML = currencySign + subtotal.toFixed(2);
        }
        const cartTex = elm.parentElement.nextElementSibling.querySelector(".totalTable .tTable .cart-tax")
        if (cartTex) {
            cartTex.innerHTML = currencySign + tax.toFixed(2);
        }
        const cartshipping = elm.parentElement.nextElementSibling.querySelector(".totalTable .tTable .cart-shipping")
        if (cartshipping) {
            cartshipping.innerHTML = currencySign + shipping.toFixed(2);
        }
        const carttotal = elm.parentElement.nextElementSibling.querySelector(".totalTable .tTable .cart-total")
        if (carttotal) {
            carttotal.innerHTML = currencySign + newTotal.toFixed(2);
        }
        const cartdiscount = elm.parentElement.nextElementSibling.querySelector(".totalTable .tTable .cart-discount")
        if (cartdiscount) {
            cartdiscount.innerHTML = "-" + currencySign + discount.toFixed(2);
        }
    }
}
//input spinner end
inputSpinComponets()
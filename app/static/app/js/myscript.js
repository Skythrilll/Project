$(document).ready(function () {
    console.log('=== Cart JavaScript loaded - Version 2.0 ===');
    console.log('jQuery version:', $.fn.jquery);
    console.log('Plus buttons found:', $('.plus-cart').length);
    console.log('Minus buttons found:', $('.minus-cart').length);
    console.log('Remove buttons found:', $('.remove-cart').length);

    // Test if buttons have pid attribute
    $('.plus-cart').each(function (index) {
        console.log('Plus button ' + index + ' pid:', $(this).attr('pid'));
    });

    // Use event delegation for dynamically loaded content
    $(document).on('click', '.plus-cart', function (e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('Plus button clicked!');
        var id = $(this).attr('pid');
        console.log('Product ID:', id);
        if (!id) {
            console.error('No pid attribute found');
            return;
        }
        var eml = $('#quantity' + id);
        console.log('Quantity element found:', eml.length > 0);
        $.ajax({
            type: "GET",
            url: "/pluscart/",
            data: {
                prod_id: id
            },
            success: function (data) {
                console.log("Plus success - data = ", data);
                eml.text(data.quantity);
                $("#amount").text("€" + data.amount);
                $("#totalamount").text("€" + data.totalamount);
                // Update navbar cart count
                var cartLink = $('a[href*="showcart"]');
                var cartBadge = cartLink.find('.badge.bg-danger');
                if (data.cart_count > 0) {
                    if (cartBadge.length > 0) {
                        cartBadge.text(data.cart_count);
                    } else {
                        cartLink.prepend('<span class="badge bg-danger">' + data.cart_count + '</span> ');
                    }
                } else {
                    cartBadge.remove();
                }
            },
            error: function (xhr, status, error) {
                console.error("Plus error: " + error);
                console.error("Response: ", xhr.responseText);
            }
        });
    });

    $(document).on('click', '.minus-cart', function (e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('Minus button clicked!');
        var id = $(this).attr('pid');
        console.log('Product ID:', id);
        if (!id) {
            console.error('No pid attribute found');
            return;
        }
        var eml = $('#quantity' + id);
        console.log('Quantity element found:', eml.length > 0);
        $.ajax({
            type: "GET",
            url: "/minuscart/",
            data: {
                prod_id: id
            },
            success: function (data) {
                console.log("Minus success - data = ", data);
                if (data.quantity <= 0) {
                    // Remove the item from DOM if quantity is 0
                    eml.closest('.row.mb-4').fadeOut(300, function () {
                        $(this).remove();
                        // Check if cart is empty
                        if ($('.card-body .row.mb-4').length === 0) {
                            location.reload();
                        }
                    });
                } else {
                    eml.text(data.quantity);
                }
                $("#amount").text("€" + data.amount);
                $("#totalamount").text("€" + data.totalamount);
                // Update navbar cart count
                var cartLink = $('a[href*="showcart"]');
                var cartBadge = cartLink.find('.badge.bg-danger');
                if (data.cart_count > 0) {
                    if (cartBadge.length > 0) {
                        cartBadge.text(data.cart_count);
                    } else {
                        cartLink.prepend('<span class="badge bg-danger">' + data.cart_count + '</span> ');
                    }
                } else {
                    cartBadge.remove();
                }
            },
            error: function (xhr, status, error) {
                console.error("Minus error: " + error);
                console.error("Response: ", xhr.responseText);
            }
        });
    });
});

$(document).ready(function () {
    $('.remove-cart').click(function (e) {
        e.preventDefault();
        var id = $(this).attr('pid').toString();
        var itemRow = $(this).closest('.row.mb-4');
        console.log('removing pid = ', id);

        if (confirm('Are you sure you want to remove this item from cart?')) {
            $.ajax({
                type: "GET",
                url: "/removecart/",
                data: {
                    prod_id: id
                },
                success: function (data) {
                    console.log("data = ", data);
                    // Remove item from DOM with fade effect
                    itemRow.fadeOut(300, function () {
                        $(this).remove();
                        // Update totals
                        $("#amount").text("€" + data.amount);
                        $("#totalamount").text("€" + data.totalamount);
                        // Update navbar cart count
                        var cartLink = $('a[href*="showcart"]');
                        var cartBadge = cartLink.find('.badge.bg-danger');
                        if (data.cart_count > 0) {
                            if (cartBadge.length > 0) {
                                cartBadge.text(data.cart_count);
                            } else {
                                cartLink.prepend('<span class="badge bg-danger">' + data.cart_count + '</span> ');
                            }
                        } else {
                            cartBadge.remove();
                        }

                        // Check if cart is empty and reload page
                        if ($('.card-body .row.mb-4').length === 0) {
                            location.reload();
                        }
                    });
                }
            });
        }
    });
});

$(document).on('click', '.plus-wishlist', function (e) {
    e.preventDefault();
    var id = $(this).attr('pid').toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist/",
        data: {
            prod_id: id
        },
        success: function (data) {
            window.location.reload();
        }
    });
});

$(document).on('click', '.minus-wishlist', function (e) {
    e.preventDefault();
    var id = $(this).attr('pid').toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist/",
        data: {
            prod_id: id
        },
        success: function (data) {
            window.location.reload();
        }
    });
});

// Add to cart functionality
$(document).on('click', '.add-to-cart', function (e) {
    e.preventDefault();
    var id = $(this).attr('pid').toString();
    $.ajax({
        type: "GET",
        url: "/add-to-cart/",
        data: {
            prod_id: id
        },
        success: function (data) {
            console.log("Product added to cart:", data);
            // Update cart count in navbar - find the cart link
            var cartLink = $('a[href*="showcart"]');
            var cartBadge = cartLink.find('.badge.bg-danger');

            if (data.cart_count > 0) {
                if (cartBadge.length > 0) {
                    cartBadge.text(data.cart_count).show();
                } else {
                    // Create badge if it doesn't exist
                    cartLink.prepend('<span class="badge bg-danger">' + data.cart_count + '</span> ');
                }
            } else {
                cartBadge.remove();
            }
            // Show success message
            alert('Product added to cart!');
        },
        error: function (xhr, status, error) {
            console.error("Error adding to cart:", error);
            alert('Please login to add items to cart');
        }
    });
});


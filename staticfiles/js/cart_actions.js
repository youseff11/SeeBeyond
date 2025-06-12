document.addEventListener('DOMContentLoaded', function() {

    // Function to get CSRF token for POST requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Function to update cart count in the navbar
    function updateNavbarCartCount(newCount) {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = newCount;
            // Add a temporary animation to indicate update
            cartCountElement.classList.add('updated');
            setTimeout(() => {
                cartCountElement.classList.remove('updated');
            }, 300);
        }
    }

    // --- Quantity Update Logic ---
    document.querySelectorAll('.quantity-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const action = this.dataset.action; // 'increase' or 'decrease'
            const quantityInput = this.closest('.cart-item-details').querySelector('.quantity-input');
            let currentQuantity = parseInt(quantityInput.value);

            if (action === 'increase') {
                currentQuantity++;
            } else if (action === 'decrease' && currentQuantity > 1) {
                currentQuantity--;
            } else if (action === 'decrease' && currentQuantity === 1) {
                // If quantity becomes 0, ask to remove item
                if (confirm('Are you sure you want to remove this item from your cart?')) {
                    handleRemoveItem(productId);
                    return; // Exit to prevent quantity update
                } else {
                    return; // User cancelled, do nothing
                }
            } else {
                return; // Do nothing if quantity is 1 and trying to decrease
            }

            // Update local input first
            quantityInput.value = currentQuantity;

            // Send request to server to update quantity
            fetch('/update-cart-item/', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ 'product_id': productId, 'quantity': currentQuantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update subtotal for the item
                    const subtotalElement = this.closest('.cart-item-details').querySelector('.item-subtotal');
                    if (subtotalElement) {
                        subtotalElement.textContent = `Subtotal: $${data.item_subtotal}`;
                    }
                    // Update total cart value
                    const cartTotalElement = document.getElementById('cart-total-value');
                    if (cartTotalElement) {
                        cartTotalElement.textContent = `$${data.cart_total}`;
                    }
                    updateNavbarCartCount(data.cart_count); // Update count in navbar
                } else {
                    alert('Error updating quantity: ' + data.message);
                    // Revert quantity if update failed
                    quantityInput.value = currentQuantity - (action === 'increase' ? 1 : -1);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating the cart.');
                // Revert quantity on error
                quantityInput.value = currentQuantity - (action === 'increase' ? 1 : -1);
            });
        });
    });

    // --- Quantity Input Change Logic (if user types) ---
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('change', function() {
            const productId = this.dataset.productId;
            let newQuantity = parseInt(this.value);

            if (isNaN(newQuantity) || newQuantity < 1) {
                alert('Please enter a valid quantity (1 or more).');
                // You might want to revert to a previous valid quantity or re-fetch from server
                return;
            }

            // Send request to server to update quantity
            fetch('/update-cart-item/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ 'product_id': productId, 'quantity': newQuantity })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.value = newQuantity; // Ensure input reflects the sent quantity
                    const subtotalElement = this.closest('.cart-item-details').querySelector('.item-subtotal');
                    if (subtotalElement) {
                        subtotalElement.textContent = `Subtotal: $${data.item_subtotal}`;
                    }
                    const cartTotalElement = document.getElementById('cart-total-value');
                    if (cartTotalElement) {
                        cartTotalElement.textContent = `$${data.cart_total}`;
                    }
                    updateNavbarCartCount(data.cart_count);
                } else {
                    alert('Error updating quantity: ' + data.message);
                    // Optionally revert input value if update failed
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating the cart.');
            });
        });
    });


    // --- Remove Item Logic ---
    document.querySelectorAll('.btn-remove-item').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            if (confirm('Are you sure you want to remove this item from your cart?')) {
                handleRemoveItem(productId);
            }
        });
    });

    function handleRemoveItem(productId) {
        fetch('/remove-from-cart/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ 'product_id': productId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the item's HTML element from the DOM
                const itemElement = document.getElementById(`cart-item-${productId}`);
                if (itemElement) {
                    itemElement.remove();
                }

                // Update total cart value
                const cartTotalElement = document.getElementById('cart-total-value');
                if (cartTotalElement) {
                    cartTotalElement.textContent = `$${data.cart_total}`;
                }

                updateNavbarCartCount(data.cart_count); // Update count in navbar

                // If cart is empty, show empty message and hide total/checkout
                if (data.cart_count === 0) {
                    const cartItemsContainer = document.querySelector('.cart-items-container');
                    const emptyMessage = document.getElementById('empty-cart-message');
                    const cartTotalSection = document.querySelector('.cart-total');

                    if (emptyMessage) {
                        emptyMessage.style.display = 'block'; // Show the empty message
                    } else { // If message didn't exist, create it (fallback)
                        // Note: Using Django template tags like {% url "shop" %} directly in JS is not possible without passing it from context.
                        // For simplicity, we hardcode the URL. A more robust solution might pass it from Django.
                        cartItemsContainer.innerHTML = '<p id="empty-cart-message" style="text-align: center;">Your cart is empty. <a href="/shop/">Start shopping!</a></p>';
                    }
                    if (cartTotalSection) {
                        cartTotalSection.style.display = 'none'; // Hide total and checkout button
                    }
                }
            } else {
                alert('Error removing item: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while removing the item.');
        });
    }

    // --- Confirm Order Button Logic (formerly Checkout Button) ---
    const checkoutBtn = document.querySelector('.btn-checkout'); // لازالت تستخدم نفس الـ class
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function() {
            // هنا بنرسل طلب AJAX لإنشاء الطلب في الداتابيز
            const cartTotalValueElement = document.getElementById('cart-total-value');
            // تأكد من وجود العنصر قبل محاولة قراءة قيمته
            const total = cartTotalValueElement ? parseFloat(cartTotalValueElement.textContent.replace('$', '')) : 0;

            fetch('/process-order/', { // ده الـ URL بتاع الـ process_order view
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // لازم تبعت الـ CSRF token
                },
                body: JSON.stringify({
                    'total_price': total, // هذا يُرسل كبيانات، لكن الـ backend بيعيد حسابها
                    // يمكنك إضافة أي بيانات أخرى هنا إذا كانت مطلوبة (مثل بيانات الشحن إذا كانت موجودة في فورم)
                })
            })
            .then(response => {
                if (!response.ok) {
                    // إذا لم تكن الاستجابة 2xx (مثلاً 400, 500)، ارمِ خطأ
                    return response.json().then(errorData => {
                        throw new Error(errorData.message || 'Server error');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    alert('Order placed successfully! Order ID: ' + data.order_id);
                    // توجهه لصفحة تأكيد الطلب
                    window.location.href = data.redirect_url; // ده الـ URL اللي راجع من Django View
                } else {
                    alert('Error placing order: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while placing your order: ' + error.message);
            });
        });
    }

    // Initial check for empty cart on load (if rendered with 0 items)
    const cartItemsContainer = document.querySelector('.cart-items-container');
    const emptyMessage = document.getElementById('empty-cart-message');
    const cartTotalSection = document.querySelector('.cart-total');

    if (cartItemsContainer && cartItemsContainer.children.length > 0) {
        // Check if there are any actual cart-item elements inside the container
        const actualCartItems = cartItemsContainer.querySelectorAll('.cart-item');
        if (actualCartItems.length === 0 && emptyMessage) {
            emptyMessage.style.display = 'block';
            if (cartTotalSection) {
                cartTotalSection.style.display = 'none';
            }
        } else if (emptyMessage) { // There are items, ensure empty message is hidden
            emptyMessage.style.display = 'none';
            if (cartTotalSection) {
                cartTotalSection.style.display = 'block';
            }
        }
    } else if (emptyMessage) { // Container might be empty or not found, assume cart is empty
        emptyMessage.style.display = 'block';
        if (cartTotalSection) {
            cartTotalSection.style.display = 'none';
        }
    }
});
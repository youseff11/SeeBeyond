document.addEventListener('DOMContentLoaded', function() {
    const addToCartButton = document.querySelector('.btn-add-to-cart');
    const shoppingBagIcon = document.querySelector('.nav-right img[alt="Shopping Bag"]'); 
    const cartCountElement = document.getElementById('cart-count'); 

    const LOGIN_PAGE_URL = '/login/'; 

    if (!cartCountElement) {
        console.warn("Element with ID 'cart-count' not found. Cart count will not update.");
    }

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

    if (addToCartButton) {
        addToCartButton.addEventListener('click', function(event) {
            event.preventDefault(); 
            const productId = this.dataset.productId; 
            const csrftoken = getCookie('csrftoken');

            fetch('/add-to-cart/', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ 'product_id': productId })
            })
            .then(response => {
                return response.json().then(data => {
                    if (response.status === 401) {
                        alert(data.message); 
                        window.location.href = LOGIN_PAGE_URL; 
                        return Promise.reject('User not authenticated, redirecting to login.'); 
                    }
                    return { data: data, response: response }; 
                });
            })
            .then(result => {
                const data = result.data;
                const response = result.response;

                if (response.ok && data.success) { 
                    alert(data.message); 
                    if (cartCountElement) {
                        cartCountElement.textContent = data.cart_count; 
                    }
                    if (shoppingBagIcon) {
                        shoppingBagIcon.style.transform = 'scale(1.3)';
                        shoppingBagIcon.style.transition = 'transform 0.2s ease-in-out';
                        setTimeout(() => {
                            shoppingBagIcon.style.transform = 'scale(1)';
                        }, 300);
                    }
                } else if (data && data.message) {
                    alert('Error: ' + data.message); 
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (error !== 'User not authenticated, redirecting to login.') { 
                    alert('please login first');
                }
            });
        });
    }
});
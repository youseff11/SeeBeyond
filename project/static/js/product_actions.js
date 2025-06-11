document.addEventListener('DOMContentLoaded', function() {
    const addToCartButton = document.querySelector('.btn-add-to-cart');
    const shoppingBagIcon = document.querySelector('.nav-right img[alt="Shopping Bag"]'); // أيقونة سلة التسوق
    const cartCountElement = document.getElementById('cart-count'); // العنصر الذي سيظهر عدد المنتجات


    if (!cartCountElement) {
        console.warn("Element with ID 'cart-count' not found. Cart count will not update.");

    }


    if (addToCartButton) {
        addToCartButton.addEventListener('click', function() {
            const productId = this.dataset.productId; // الحصول على الـ ID من data-product-id

            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            const csrftoken = getCookie('csrftoken');

            fetch('/add-to-cart/', { // هذا الـ URL سنقوم بإنشائه في Django
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
                    alert(data.message); // رسالة نجاح
                    if (cartCountElement) {
                        cartCountElement.textContent = data.cart_count; // تحديث العدد
                    }
                    if (shoppingBagIcon) {
                        shoppingBagIcon.style.transform = 'scale(1.3)';
                        shoppingBagIcon.style.transition = 'transform 0.2s ease-in-out';
                        setTimeout(() => {
                            shoppingBagIcon.style.transform = 'scale(1)';
                        }, 300);
                    }

                } else {
                    alert('Error: ' + data.message); // رسالة خطأ
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('حدث خطأ أثناء إضافة المنتج للعربة.');
            });
        });
    }
});
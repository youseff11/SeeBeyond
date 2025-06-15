from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required 
import json
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash 
from decimal import Decimal
from .models import Order, OrderItem, Profile 
from products.models import Product
from .forms import CustomUserCreationForm, ProfileUpdateForm 
from django.db import transaction # استيراد المعاملات

# --- 1. User Authentication & Authorization Views ---

def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}! You are logged in.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})

def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account for {user.username} created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')

    else: # GET request
        form = CustomUserCreationForm()
    return render(request, 'pages/signup.html', {'form': form})


def user_logout(request):
    """
    Logs out the current user.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

# --- 2. General Page Views ---

def home(request):
    return render(request, 'pages/home.html')

def policies(request):
    return render(request, 'pages/policies.html')

def add_address(request):
    return render(request, 'pages/add_address.html')

# --- 3. User Account Management View ---

@login_required 
def account(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user_profile, user_instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('account') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=user_profile, user_instance=request.user)

    user_orders = Order.objects.filter(user=request.user).order_by('-date_ordered')

    context = {
        'form': form,
        'user': request.user,
        'orders': user_orders,
    }
    return render(request, 'pages/account.html', context)


# --- 4. Cart Management Views ---
@require_POST
def add_to_cart(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # هنا يتم إرجاع JsonResponse بـ status 401
        return JsonResponse({'success': False, 'message': 'Please log in first.'}, status=401) # 401 Unauthorized

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')

        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required.'}, status=400)

        try:
            product = get_object_or_404(Product, id=product_id)
        except Exception:
            return JsonResponse({'success': False, 'message': 'Product not found.'}, status=404)

        cart = request.session.get('cart', {})
        product_id_str = str(product.id)

        if product_id_str in cart:
            cart[product_id_str]['quantity'] += 1
        else:
            cart[product_id_str] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 1,
                'image_url': product.image.url if product.image else ''
            }

        request.session['cart'] = cart
        request.session.modified = True

        cart_count = sum(item['quantity'] for item in cart.values())

        return JsonResponse({'success': True, 'message': f'{product.name} added to cart.', 'cart_count': cart_count})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON request.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

def cart_summary_view(request):
    cart_session_data = request.session.get('cart', {})
    cart_items = []
    cart_total = Decimal('0.00')

    for product_id_str, item_data in cart_session_data.items():
        try:
            item_price = Decimal(item_data['price'])
            item_quantity = int(item_data['quantity'])

            if item_quantity <= 0:
                continue

            subtotal = item_price * item_quantity
            cart_total += subtotal

            cart_items.append({
                'product_id': product_id_str,
                'name': item_data['name'],
                'price': item_price,
                'quantity': item_quantity,
                'image_url': item_data['image_url'],
                'subtotal': subtotal.quantize(Decimal('0.01'))
            })
        except Exception as e:
            print(f"Error processing cart item {product_id_str}: {e}")
            continue

    context = {
        'cart': cart_items,
        'cart_total': cart_total.quantize(Decimal('0.01'))
    }
    return render(request, 'pages/cart_summary.html', context)

@require_POST
def update_cart_item(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        new_quantity = int(data.get('quantity'))

        if not product_id or new_quantity is None:
            return JsonResponse({'success': False, 'message': 'Product ID and quantity are required.'}, status=400)

        cart = request.session.get('cart', {})
        product_id_str = str(product_id)

        if product_id_str not in cart:
            return JsonResponse({'success': False, 'message': 'Item not in cart.'}, status=404)

        if new_quantity <= 0:
            del cart[product_id_str]
        else:
            cart[product_id_str]['quantity'] = new_quantity

        request.session['cart'] = cart
        request.session.modified = True

        cart_count = sum(item['quantity'] for item in cart.values())
        cart_total = sum(Decimal(item['price']) * item['quantity'] for item in cart.values())
        item_subtotal = Decimal('0.00')

        if product_id_str in cart:
            item_subtotal = Decimal(cart[product_id_str]['price']) * cart[product_id_str]['quantity']

        return JsonResponse({
            'success': True,
            'message': 'Cart updated.',
            'cart_count': cart_count,
            'cart_total': cart_total.quantize(Decimal('0.01')),
            'item_subtotal': item_subtotal.quantize(Decimal('0.01'))
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON request.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@require_POST
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')

        if not product_id:
            return JsonResponse({'success': False, 'message': 'Product ID is required.'}, status=400)

        cart = request.session.get('cart', {})
        product_id_str = str(product_id)

        if product_id_str in cart:
            del cart[product_id_str]
            request.session['cart'] = cart
            request.session.modified = True

            cart_count = sum(item['quantity'] for item in cart.values())
            cart_total = sum((Decimal(item['price']) * item['quantity'] for item in cart.values()), start=Decimal('0.00'))

            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart.',
                'cart_count': cart_count,
                'cart_total': cart_total.quantize(Decimal('0.01'))
            })
        else:
            return JsonResponse({'success': False, 'message': 'Item not found in cart.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON request.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# --- 5. Order Processing Views ---
@require_POST
def process_order(request):
    transaction_id = request.POST.get('transaction_id', None)

    if request.user.is_authenticated:
        customer = request.user
    else:
        customer = None

    cart = request.session.get('cart', {})
    if not cart:
        return JsonResponse({'success': False, 'message': 'Your cart is empty. Cannot process an empty order.'}, status=400)

    try:
        with transaction.atomic():  # ابدأ المعاملة هنا
            order = Order.objects.create(
                user=customer,
                status='pending',  # ← الحالة الجديدة بدلاً من complete
                transaction_id=transaction_id,
                total_price=Decimal('0.00')
            )

            calculated_total_price = Decimal('0.00')
            problematic_products = []

            for product_id_str, item_data in cart.items():
                try:
                    product = Product.objects.get(id=int(product_id_str))
                    quantity = int(item_data['quantity'])
                    price_at_order = product.price

                    if quantity <= 0:
                        continue

                    OrderItem.objects.create(
                        product=product,
                        order=order,
                        quantity=quantity,
                        price_at_order=price_at_order
                    )
                    calculated_total_price += (price_at_order * quantity)
                except Product.DoesNotExist:
                    problematic_products.append(f"Product with ID {product_id_str} not found.")
                    print(f"Product with ID {product_id_str} not found during order processing, skipping.")
                except Exception as e:
                    problematic_products.append(f"Error for product ID {product_id_str}: {e}")
                    print(f"Error creating OrderItem for product {product_id_str}: {e}")

            if problematic_products:
                raise Exception(f"Failed to process order due to issues with some products: {'; '.join(problematic_products)}")

            order.total_price = calculated_total_price.quantize(Decimal('0.01'))
            # هنا ممكن تخليها تفضل "pending"، أو تغيرها حسب منطقتك اللوجستية
            order.save()

            # حذف السلة من الجلسة
            del request.session['cart']
            request.session.modified = True

            messages.success(request, 'Your order has been placed successfully!')
            return JsonResponse({
                'success': True,
                'order_id': order.id,
                'redirect_url': f'/order-confirmation/{order.id}/'
            })

    except Exception as e:
        messages.error(request, 'There was an error processing your order. Please try again.')
        print(f"Order processing error: {e}")
        return JsonResponse({'success': False, 'message': f'Error processing order: {str(e)}'}, status=500)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user.is_authenticated and order.user != request.user:
        messages.error(request, 'You are not authorized to view this order.')
        return redirect('home')
    order_items = order.orderitem_set.all()

    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'pages/order_confirmation.html', context)
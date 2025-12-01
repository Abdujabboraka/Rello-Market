from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction
from .bot import send_to_admin

from .models import User, Category, Product, Cart, CartItem, Order, OrderItem


# ========================= HOME PAGE =============================

def homepage(request):
    categories = Category.objects.all()
    products = Product.objects.all().order_by('-id')

    # SEARCH
    q = request.GET.get("q")
    if q:
        products = products.filter(name__icontains=q)

    # FILTER BY CATEGORY
    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # PAGINATION
    paginator = Paginator(products, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home/index.html", {
        "page_obj": page_obj,
        "categories": categories,
        "q": q,
        "category_slug": category_slug,
    })


# ========================= PRODUCT DETAIL =============================

def product_detail(request, link):
    product = get_object_or_404(Product, link=link)
    return render(request, "detail.html", {"product": product})


# ========================= CATEGORY PAGE =============================

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category).order_by("-id")

    paginator = Paginator(products, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home/category_products.html", {
        "category": category,
        "page_obj": page_obj
    })


# ========================= CART FUNCTIONS =============================

def get_or_create_cart(request):
    # If logged in → user cart
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart

    # Anonymous → session cart
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def add_to_cart(request, link):
    if request.method == "POST":
        product = get_object_or_404(Product, link=link)
        cart = get_or_create_cart(request)

        item, created = CartItem.objects.get_or_create(
            cart_id=cart,
            product=product,
            defaults={"quantity": 1}
        )

        if not created:
            item.quantity += 1
            item.save()

        return JsonResponse({"status": "ok", "message": "Added"})

    return JsonResponse({"status": "error"})


def cart_page(request):
    cart = get_or_create_cart(request)
    items = CartItem.objects.filter(cart_id=cart)

    total = sum(i.product.price * i.quantity for i in items)

    return render(request, "cart.html", {
        "items": items,
        "total": total,
    })


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CartItem

def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    action = request.GET.get("action")

    if action == "plus":
        item.quantity += 1
        item.save()
    elif action == "minus":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            return JsonResponse({'status': 'ok', 'quantity': 0})

    return JsonResponse({'status': 'ok', 'quantity': item.quantity})



def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart_page")


def clear_cart(request):
    cart = get_or_create_cart(request)
    CartItem.objects.filter(cart_id=cart).delete()
    return redirect("cart_page")


# ========================= ORDER =============================

def order_page(request):
    cart = get_or_create_cart(request)
    items = CartItem.objects.filter(cart_id=cart)

    if not items:
        return redirect("cart_page")

    total_price = sum(float(i.product.price) * int(i.quantity) for i in items)

    return render(request, "order.html", {
        "items": items,
        "total": total_price
    })


def make_order(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        user_name = request.POST.get("user_name")
        cart = get_or_create_cart(request)
        items = CartItem.objects.filter(cart_id=cart)

        if not items:

            return redirect("cart_page")

        total_price = sum(float(i.product.price) * (i.quantity) for i in items)



        # CREATE ORDER
        order = Order.objects.create(
            user_name=user_name,
            phone=phone,
            address=address,
            total_price=total_price,
            status="kutilmoqda"
        )

        # SAVE ORDER ITEMS
        for i in items:
            OrderItem.objects.create(
                order_id=order,
                product_id=i.product,
                quantity=i.quantity,
                price=i.product.price
            )

        # CLEAR CART
        # items.delete()
        goods = OrderItem.objects.filter(order_id = order)
        # TODO: SEND TO TELEGRAM ADMIN BOT HERE
        order_items = ""
        for i in items:
            order_items += f"{i.quantity}x {i}   ${i.quantity * i.product.price}\n"

        order_items += f"\ntotal price: ${total_price}"
        # prepare message for telegram:
        order_info = f"""username: {user_name}\n
name: {name}
phone: {phone}\n
address: {address}\n"""

        products = order_items
        send_to_admin(order_info)
        send_to_admin(products)

        return render(request, "order_success.html", {"order": order, 'items': goods})

    return redirect("order_page")


# ========================= CONTACT =============================

def contact(request):
    return render(request, "contact.html")

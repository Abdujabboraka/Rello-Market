from django.urls import path
from .views import (
    homepage,
    add_to_cart,
    cart_page,
    remove_cart_item,
    update_quantity,
    clear_cart,
    order_page,
    make_order,
    product_detail,
    contact,
    category_products,
)

urlpatterns = [
    # Home / Katalog
    path('', homepage, name='homepage'),
    path('product/<str:link>/', product_detail, name='product_detail'),



    # Category products
    path('category/<slug:slug>/', category_products, name='category_products'),

    # Cart
    path("cart/", cart_page, name="cart_page"),
    path("cart/add/<str:link>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", remove_cart_item, name="remove_cart_item"),
    path("cart/update/<int:item_id>/", update_quantity, name="update_quantity"),

    path("cart/clear/", clear_cart, name="clear_cart"),

    # Order
    path("order/", order_page, name="order_page"),
    path("order/make/", make_order, name="make_order"),

    # Contact
    path("contact/", contact, name="contact"),
]

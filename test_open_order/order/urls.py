from django.urls import path
from .views import OrderListCreateView, OrderItemListCreateView

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    path(
        "orders/<int:order_id>/items/",
        OrderItemListCreateView.as_view(),
        name="order-item-list-create",
    ),
]

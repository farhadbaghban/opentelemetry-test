import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem

USER_SERVICE_URL = "http://users-service:8000/api/users/"

class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all().values("id", "user_id", "created_at", "status")
        return Response(list(orders))

class OrderDetailView(APIView):
    def get(self, request, pk):
        try:
            order = Order.objects.prefetch_related("items").get(id=pk)
            user_response = requests.get(f"{USER_SERVICE_URL}{order.user_id}/")
            user_data = user_response.json() if user_response.status_code == 200 else {}
            items = order.items.values("product_name", "quantity", "price")
            data = {
                "id": order.id,
                "user": user_data,
                "created_at": order.created_at,
                "status": order.status,
                "items": list(items)
            }
            return Response(data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)


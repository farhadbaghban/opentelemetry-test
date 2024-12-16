import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "customer_name", "total_price", "created_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product_name", "quantity", "price"]


USER_SERVICE_URL = "http://localhost:8000/api/user/get"


class OrderListCreateView(APIView):
    def get_user_from_service(self, user_id):
        """
        Fetch user data from the external service using the user ID.
        """
        try:
            # Assuming the user service returns a user with id and firstname
            response = requests.get(f"{USER_SERVICE_URL}/{user_id}")
            response.raise_for_status()
            user_data = response.json()
            return user_data
        except requests.exceptions.RequestException:
            return None

    def get(self, request, *args, **kwargs):
        """
        Get the list of orders.
        """
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new order. User data is fetched from the external service.
        """
        user_id = request.data.get("user_id")
        user_data = self.get_user_from_service(user_id)

        if not user_data:
            return Response(
                {"error": "User data not found or service unavailable."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If user data exists, create the order
        customer_name = user_data.get("firstname")
        data = {
            "user_id": user_id,
            "customer_name": customer_name,
            "total_price": request.data.get("total_price"),
        }
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Get the list of order items for a specific order.
        """
        order_id = self.kwargs.get("order_id")
        order = Order.objects.get(id=order_id)
        items = order.items.all()
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new order item for a specific order.
        """
        order_id = self.kwargs.get("order_id")
        order = Order.objects.get(id=order_id)
        data = request.data
        data["order"] = order.id
        serializer = OrderItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

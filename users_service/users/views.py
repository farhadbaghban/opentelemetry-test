from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class UserDetailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            data = {"id": user.id, "username": user.username, "email": user.email}
            return Response(data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


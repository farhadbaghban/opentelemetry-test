from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from opentelemetry import trace

tracer = trace.get_tracer("django-app")


class UserView(APIView):
    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = "__all__"

    def get(self, request, *args, **kwargs):
        try:
            with tracer.start_as_current_span("user_get_span"):
                pk = self.kwargs.get("pk", None)
                if pk:
                    user = User.objects.get(pk=pk)
                    serializer = self.OutPutSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    users = User.objects.all()
                    serializer = self.OutPutSerializer(users, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)

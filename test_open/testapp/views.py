from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
# from opentelemetry import trace

# tracer = trace.get_tracer("django-app")


class UserView(APIView):
    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = "__all__"

    def get(self, request, *args, **kwargs):
        try:
            # with tracer.start_as_current_span("manual-span"):
            pk = self.kwargs.get("pk", None)
            if pk:
                user = User.objects.get(pk=pk)
                return Response(
                    self.OutPutSerializer(data=user), status=status.HTTP_200_OK
                )
            else:
                users = User.objects.all()
                return Response(
                    self.OutPutSerializer(data=users, many=True),
                    status=status.HTTP_200_OK,
                )
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)

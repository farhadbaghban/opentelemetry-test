from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from .models import RequestResponse


class ReqRes(APIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = RequestResponse
            fields = "__all__"

    def get(self, request, *args, **kwargs):
        records = RequestResponse.objects.all()
        serializer = self.OutputSerializer(records, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def delete(self,request,*args, **kwargs):
        RequestResponse.objects.all().delete()
        return Response("deleted all records",status=status.HTTP_204_NO_CONTENT)
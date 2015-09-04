from django.db import IntegrityError

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from trickers.serializers import RegisterTrickerSerializer
from trickers.models import Tricker


class RegisterTrickerView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegisterTrickerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            new_tricker = Tricker.objects.create_user(**serializer.data)
            token = Token.objects.create(user=new_tricker)
            resp = {
                "id": new_tricker.pk,
                "token": token.key
            }
            return Response(resp, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT)

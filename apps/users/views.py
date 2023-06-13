from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer
from rest_framework.response import Response
from drf_util.decorators import serialize_decorator


class UserRegisterView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @serialize_decorator(UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

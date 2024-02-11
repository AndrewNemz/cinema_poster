from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.models import User
from users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

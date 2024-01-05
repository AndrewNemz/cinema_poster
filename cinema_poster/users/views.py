from djoser.views import UserViewSet
from .serializers import CustomUserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

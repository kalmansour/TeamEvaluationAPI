from .serializers import UserAdminRegisterSerializer
from rest_framework.generics import CreateAPIView

class UserAdminRegister(CreateAPIView):
    serializer_class = UserAdminRegisterSerializer
from .serializers import UserAdminRegisterSerializer,MyTokenObtainPairSerializer
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

class UserAdminRegister(CreateAPIView):
    serializer_class = UserAdminRegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
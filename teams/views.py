from .serializers import CreateSemesterSerializer, UserAdminRegisterSerializer,MyTokenObtainPairSerializer,SemesterListSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser

from .models import Semester

class UserAdminRegister(CreateAPIView):
    serializer_class = UserAdminRegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class SemesterListView(ListAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterListSerializer

class CreateSemesterView(CreateAPIView):
    serializer_class = CreateSemesterSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)
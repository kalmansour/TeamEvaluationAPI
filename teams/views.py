from .serializers import CreateSemesterSerializer, UserAdminRegisterSerializer,MyTokenObtainPairSerializer,SemesterListSerializer, ProjectListSerializer, CreateProjectSerializer, TeamListSerializer, CreateTeamSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser

from .models import Semester, Project, Team

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

class ProjectListView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

class CreateProjectView(CreateAPIView):
    serializer_class = CreateProjectSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer ):
        semester = Semester.objects.get(id=self.kwargs['semester_id'])
        serializer.save(semester=semester)

class TeamListView(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamListSerializer

class CreateTeamView(CreateAPIView):
    serializer_class = CreateTeamSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer ):
        project = Project.objects.get(id=self.kwargs['project_id'])
        serializer.save(project=project)
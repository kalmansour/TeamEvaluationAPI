from .serializers import CreateSemesterSerializer, ProjectDetailsSerializer, UserAdminRegisterSerializer,MyTokenObtainPairSerializer,SemesterListSerializer, ProjectListSerializer, CreateProjectSerializer, TeamListSerializer, CreateTeamSerializer,CriteriaListSerializer,CreateCriteriaSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt



from .models import Semester, Project, Team, Criteria

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

class ProjectDetailsView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'project_id'

class CreateProjectViewSet(viewsets.ModelViewSet):
    serializer_class = CreateProjectSerializer
    permission_classes = [IsAdminUser]

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        data = request.data

        new_project = Project.objects.create(
            name=data["name"], weight=data['weight'], semester =Semester.objects.get(id=self.kwargs['semester_id']) )

        new_project.save()

        for criteria in data["criteria"]:
            criteria_obj = Criteria.objects.get(name=criteria)
            new_project.criteria.add(criteria_obj)

        serializer = CreateProjectSerializer(new_project)

        return Response(serializer.data)

class TeamListView(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamListSerializer

class CreateTeamView(CreateAPIView):
    serializer_class = CreateTeamSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer ):
        project = Project.objects.get(id=self.kwargs['project_id'])
        serializer.save(project=project)

class CriteriaListView(ListAPIView):
    queryset = Criteria.objects.all()
    serializer_class = CriteriaListSerializer

class CreateCriteriaView(CreateAPIView):
    serializer_class = CreateCriteriaSerializer
    permission_classes = [IsAdminUser]


from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from teams.models import Criteria, Semester, Project, Team, CriteriaScore

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name']

class SemesterListSerializer(serializers.ModelSerializer):
    added_by = UserSerializer()
    class Meta:
        model = Semester
        fields = ['id', 'name', 'added_by']

class CreateSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['name']

class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = ['id', 'name', 'weight']

class ProjectListSerializer(serializers.ModelSerializer):
    semester = SemesterListSerializer()
    criteria = CriteriaSerializer(many=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'weight', 'semester', 'criteria']

class ProjectDetailsSerializer(serializers.ModelSerializer):
    semester = SemesterListSerializer()
    criteria = CriteriaSerializer(many=True)
    detail = serializers.HyperlinkedIdentityField(
        view_name = "project-details",
        lookup_field = "id",
        lookup_url_kwarg = "project_id"
        )
    class Meta:
        model = Project
        fields = ['id', 'name', 'weight', 'semester', 'criteria','detail']

class CreateProjectSerializer(serializers.ModelSerializer):
    criteria = CriteriaSerializer(many=True)
    class Meta:
        model = Project
        fields = ['name', 'weight', 'criteria']

class TeamListSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer()
    class Meta:
        model = Team
        fields = ['id', 'name', 'members', 'project']

class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'members']

class CriteriaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = ['id', 'name', 'weight']

class CreateCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criteria
        fields = ['name', 'weight']
        
class UserAdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password']
        

    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.is_staff = True
        new_user.save()
        return validated_data

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        # ...

        return token

class CreateCriteriaScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CriteriaScore
        fields = ['score','judge', 'note']

class CriteriaScoreListSerializer(serializers.ModelSerializer):
    criteria = CriteriaListSerializer()
    criteria_score = serializers.SerializerMethodField()
    class Meta:
        model = CriteriaScore
        fields = ['id', 'team', 'criteria','judge', 'score','note','criteria_score']

    def get_criteria_score(self, obj):
        average_score = obj.score/ obj.criteria.weight *100
        return {'name': str(obj.criteria), 'average_score': average_score,'weight':obj.criteria.weight, 'weighted_average' : obj.score}


                

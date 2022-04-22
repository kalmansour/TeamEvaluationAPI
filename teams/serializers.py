from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from teams.models import Semester, Project, Team

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

class ProjectListSerializer(serializers.ModelSerializer):
    semester = SemesterListSerializer()
    class Meta:
        model = Project
        fields = ['id', 'name', 'weight', 'semester']

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'weight']

class TeamListSerializer(serializers.ModelSerializer):
    project = ProjectListSerializer()
    class Meta:
        model = Team
        fields = ['id', 'name', 'members', 'project']

class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'members']
        
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

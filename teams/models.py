from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class Semester(models.Model):
    name = models.CharField(max_length=120)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Criteria(models.Model):
    name = models.CharField(max_length=120)
    weight = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=120)
    weight = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="projects")
    criteria = models.ManyToManyField(Criteria)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=120)
    members = models.CharField(max_length=120)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="teams")

    def __str__(self):
        return self.name

class CriteriaScore(models.Model):
    judge = models.CharField(max_length=12)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="score")
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE, related_name="score")
    score = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    note =  models.TextField()

    def __str__(self):
        return "%s: %s" % (self.criteria.name, str(self.score))

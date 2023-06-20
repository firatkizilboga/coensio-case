from django.db import models

# Create your models here.

class Exam(models.Model):
    profession = models.CharField(max_length=300)
    def __str__(self):
        return self.profession

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    is_multiple_choice = models.BooleanField(default=False)
    is_free_text = models.BooleanField(default=False)
    a = models.CharField(max_length=300)
    b = models.CharField(max_length=300)
    c = models.CharField(max_length=300)
    d = models.CharField(max_length=300)
    answer = models.CharField(max_length=8000)
    id_in_exam = models.IntegerField(default=0)
    
    def __str__(self):
        return self.question_text
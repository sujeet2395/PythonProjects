from django.db import models

# Create your models here.
class Question(models.Model):
    type=models.CharField(max_length=100)
    question=models.CharField(max_length=250)
    
    def str(self):
        return str(self.id+': '+self.type+': '+self.question)

class DareShared(models.Model):
    creator_name=models.CharField(max_length=100)
    ques_selected_str=models.CharField(max_length=100)
    
    def str(self):
        return str(self.creator_name+": "+self.ques_selected_str)
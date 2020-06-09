from django.db import models
from DareYou.models import Question
import json

# Create your models here.
class User(models.Model):
    user_name=models.CharField(max_length=100)
    def str(self):
        return self.user_name
    def __repr__(self):
        return json.dumps(self.__dict__)
    
class CnfBox(models.Model):
    quiz_id=models.CharField(max_length=100)
    creator=models.ForeignKey(User, on_delete=models.CASCADE)
    quest_selected_str=models.CharField(max_length=100)
    def str(self):
        return self.creator+": "+self.quiz_id+": "+self.ques_selected_str

class Result(models.Model):
    cnf_box=models.ForeignKey(CnfBox, on_delete=models.CASCADE)
    player=models.ForeignKey(User, on_delete=models.CASCADE)
    ans_of_cnf_box=models.CharField(max_length=250)
    
    def str(self):
        return self.cnf_box+": "+self.player+": "+self.ans_of_cnf_box

class AnsOfCnfBox(models.Model):
    result_of_quiz=models.ForeignKey(Result, on_delete=models.CASCADE)
    quest=models.ForeignKey(Question, on_delete=models.CASCADE)
    ans=models.CharField(max_length=50)
    
    def str(self):
        return self.result_of_quiz+": "+self.quest+": "+self.ans
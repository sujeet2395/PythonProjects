from django.shortcuts import render, redirect
from DareYou.models import Question
from ConfessionBox.models import User, CnfBox, AnsOfCnfBox, Result
import string
import secrets
from django.http.response import HttpResponse, JsonResponse
from rest_framework.views import APIView
from json.encoder import JSONEncoder
import json
from django.contrib import auth
from _operator import is_


# Create your views here.
def cb_home(request):
    return render(request, 'cb_home.html')

def cb_create(request):
    user_tracked={}
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        un = User.objects.get(id=user_id).user_name
        is_creator=False
        if 'is_creator' in request.session:
            is_creator = request.session['is_creator']
               
        httppart='https://'
        if request.get_host()=='127.0.0.1:8000':
            httppart='http://'
        else:
            httppart='https://'
        user_cnfbox_url=httppart+request.get_host()+'/cnfbx/user_cnfbox/'+str(user_id)+'/'
        
        user_tracked={'un': un, 'user_id': user_id, 'is_creator': is_creator, 'user_cnfbox_url': user_cnfbox_url}
        return render(request, 'cb_create.html', user_tracked)
    return render(request, 'cb_create.html')

def cb_quiz_quest(request):
    if request.method=='POST':
        un=request.POST['userName']
        if un!="":
            q_list=Question.objects.all()
            q_dict=dict()
            for q in q_list:
                q_dict[str(q.id)]=q.question.replace('<username>', un)
            cnf_quests={'un':un,'q_dict':q_dict}
            request.session['cnf_quests']=cnf_quests
            return render(request, 'cb_quiz_quest.html',cnf_quests)
    return render(request, 'cb_create.html')
        
def create_quiz(request):
    if request.method=='POST':
        if 'cnf_quests' in request.session:
            cnf_quests=request.session['cnf_quests']
            q_dict=cnf_quests['q_dict']
            un=cnf_quests['un']
        selected_q_str=request.POST['selected_q_str']
        if un!="" and selected_q_str!="":
            selected_q_id_list=selected_q_str.split(',')
            selected_q_list=dict()
            for q_id in selected_q_id_list:
                selected_q_list[q_id]=q_dict[q_id]
                
            if 'user_id' in request.session:
                user=User.objects.get(id=request.session['user_id'])
                #user=auth.authenticate(username=user.user_name, password=user.id)
                #if user is not None:
                if user.user_name!=un:
                    #user.user_name=un
                    User.objects.filter(id=request.session['user_id']).update(user_name=un)
                #    auth.login(request,user)
            else:
                user=User(user_name=un)
                user.save()
                #auth.login(request, user=user)
            quiz_id=random_secure_string()
            cnf_box=CnfBox(quiz_id=quiz_id, creator=user, quest_selected_str=selected_q_str)
            #user.save()
            cnf_box.save()
                           
            request.session['user_type']='creator'
            request.session['is_creator']=True
            request.session['user_id']=user.id
            '''
            httppart='https://'
            if request.get_host()=='127.0.0.1:8000':
                httppart='http://'
            else:
                httppart='https://'
            cnf_dare_url=httppart+request.get_host()+'/cnfbx/play_q/'+quiz_id
            result_view_url=httppart+request.get_host()+'/cnfbx/result_view/'+quiz_id
            
            cnf_dared_q={'un':un,'selected_q_list':selected_q_list,'cnf_dare_url':cnf_dare_url, 'result_view_url': result_view_url}
            return render(request, 'share_quiz.html', cnf_dared_q)
            '''
            return redirect(user_cnfbox, user_id=user.id)
    return render(request,'cb_create.html')

def user_cnfbox(request, user_id):
    if user_id > 0:
        try:
            creator=User.objects.get(id=user_id)
            if creator is None:
                raise ValueError('User not found.')
        except ValueError:
            return render(request, 'error.html')
        
        cnfboxes_query=CnfBox.objects.filter(creator=creator)
        cnfboxes = list()
        for cnfbox in cnfboxes_query:
            selected_q_id_list=cnfbox.quest_selected_str.split(',')
            selected_q_list=dict()
            for q_id in selected_q_id_list:
                selected_q_list[q_id]=Question.objects.get(id=q_id).question.replace('<username>', creator.user_name)
            cnfbox_items=dict()
            cnfbox_items['selected_q_list']=selected_q_list
            cnfbox_items['quiz_id']=cnfbox.quiz_id
            httppart='https://'
            if request.get_host()=='127.0.0.1:8000':
                httppart='http://'
            else:
                httppart='https://'
            cnf_dare_url=httppart+request.get_host()+'/cnfbx/play_q/'+cnfbox.quiz_id+'/'
            result_view_url=httppart+request.get_host()+'/cnfbx/result_view/'+cnfbox.quiz_id+'/'
            cnfbox_items['cnf_dare_url']=cnf_dare_url
            cnfbox_items['result_view_url']=result_view_url
            cnfboxes.append(cnfbox_items)
        
        request.session['user_type']='creator'
        request.session['is_creator']=True
        request.session['user_id']=user_id
        
        is_player=False
        if 'is_player' in request.session:
            is_player=request.session['is_player']
            
        return render(request, 'user_cnfboxes.html', {'cnfboxes':cnfboxes, 'un':creator.user_name, 'is_player': is_player, 'user_id': user_id})
    return render(request, 'cb_create.html')


def player(request, quiz_id):
    user_tracked={}
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        un = User.objects.get(id=user_id).user_name
        is_player = False
        if 'is_player' in request.session:
            is_player=request.session['is_player']
        httppart='https://'
        if request.get_host()=='127.0.0.1:8000':
            httppart='http://'
        else:
            httppart='https://'
        user_played_cnfbox_url=httppart+request.get_host()+'/cnfbx/user_played_cnfbox/'+str(user_id)+'/'
        user_tracked={'un': un, 'quiz_id':quiz_id, 'user_id': user_id, 'is_player': is_player, 'user_played_cnfbox_url': user_played_cnfbox_url}
        return render(request, 'player_un.html', user_tracked)
    return render(request, 'player_un.html',{'quiz_id':quiz_id})

def play_quiz(request, quiz_id):
    if request.method=='POST':
        player_un=request.POST['userName']
        cnfbox=CnfBox.objects.filter(quiz_id=quiz_id).first()
        creator=cnfbox.creator
        selected_q_id_list=cnfbox.quest_selected_str.split(',')
        selected_q_list=dict()
        for q_id in selected_q_id_list:
            selected_q_list[q_id]=Question.objects.get(id=q_id).question.replace('<username>', creator.user_name)
        
        cnf_player={'player_un':player_un, 'creator': creator,'quiz_id':quiz_id, 'selected_q_list':selected_q_list}
        request.session['player_un']=player_un
        
        return render(request, 'play_quiz.html', cnf_player)
    return render(request,'cb_create.html')

def result(request, quiz_id):
    if request.method=='POST':
        player_un=request.session['player_un']
        
        if 'user_id' in request.session:
            player=User.objects.get(id=request.session['user_id'])
            #user=auth.authenticate(username=user.user_name, password=user.id)
            #if user is not None:
            if player.user_name!=player_un:
                #user.user_name=un
                User.objects.filter(id=request.session['user_id']).update(user_name=player_un)
            #    auth.login(request,user)
        else:
            player=User(user_name=player_un)
            player.save()
            #auth.login(request, user=user)
        
        cnfbox=CnfBox.objects.filter(quiz_id=quiz_id).first()
        selected_q_id_list=cnfbox.quest_selected_str.split(',')
        
        counter=0
        ans_dict_str=""
        for q_id in selected_q_id_list:
            counter+=1
            quest=Question.objects.get(id=q_id)
            ans=request.POST['ans'+str(counter)]
            ans_dict_str+=str(q_id)+":"+ans+","
        ans_dict_str=ans_dict_str[:len(ans_dict_str)-1]
        
        result=Result(cnf_box=cnfbox, player=player, ans_of_cnf_box=ans_dict_str)
        result.save()
        
        counter=0
        for q_id in selected_q_id_list:
            counter+=1
            quest=Question.objects.get(id=q_id)
            ans=request.POST['ans'+str(counter)]
            ansofcnfbox=AnsOfCnfBox(result_of_quiz=result, quest=quest, ans=ans)
            ansofcnfbox.save()
        
        request.session['user_id']=player.id
        request.session['user_type']='player'
        request.session['is_player']=True
        return redirect(user_played_cnfbox, user_id=player.id)
    return render(request,'cb_create.html')

def user_played_cnfbox(request, user_id):
    if user_id>0:
        try:
            player=User.objects.get(id=user_id)
            if player is None:
                raise ValueError('User not found.')
        except ValueError:
            return render(request, 'error.html')
        result_query=Result.objects.filter(player=player)
        cnfboxes=list()
        for res in result_query:
            cnfbox=CnfBox.objects.get(id=res.cnf_box.id)
            creator=cnfbox.creator
            selected_q_id_list=cnfbox.quest_selected_str.split(',')
            selected_q_list=dict()
            for q_id in selected_q_id_list:
                selected_q_list[q_id]=Question.objects.get(id=q_id).question.replace('<username>', creator.user_name)
            cnfbox_items=dict()
            cnfbox_items['selected_q_list']=selected_q_list
            cnfbox_items['quiz_id']=cnfbox.quiz_id
            cnfbox_items['creator_un']=creator.user_name
            httppart='https://'
            if request.get_host()=='127.0.0.1:8000':
                httppart='http://'
            else:
                httppart='https://'
            cnf_dare_url=httppart+request.get_host()+'/cnfbx/play_q/'+cnfbox.quiz_id+'/'
            result_view_url=httppart+request.get_host()+'/cnfbx/result_view/'+cnfbox.quiz_id+'/'
            cnfbox_items['cnf_dare_url']=cnf_dare_url
            cnfbox_items['result_view_url']=result_view_url
            cnfboxes.append(cnfbox_items)
        
        request.session['user_type']='player'
        request.session['is_player']=True
        request.session['user_id']=user_id
        is_creator=False
        if 'is_creator' in request.session:
            is_creator=request.session['is_creator']
        
        return render(request, 'user_played_cnfboxes.html', {'cnfboxes':cnfboxes, 'is_creator': is_creator, 'user_id': user_id})
    return render(request, 'cb_create.html')
        
    
'''
#testing api view
class result_apiview(APIView):
    def get(self, request, quiz_id):
        return redirect(result_view, quiz_id)
    
    def post(self, request, quiz_id):
        if request.method=='POST':
            player_un=request.session['player_un']
            player=User(user_name=player_un)
            player.save()
            
            cnfbox=CnfBox.objects.filter(quiz_id=quiz_id).first()
            creator=cnfbox.creator
            selected_q_id_list=cnfbox.quest_selected_str.split(',')
            
            counter=0
            ans_dict_str=""
            for q_id in selected_q_id_list:
                counter+=1
                quest=Question.objects.get(id=q_id)
                ans=request.POST['ans'+str(counter)]
                ans_dict_str+=str(q_id)+":"+ans+","
            ans_dict_str=ans_dict_str[:len(ans_dict_str)-1]
            
            result=Result(cnf_box=cnfbox, player=player, ans_of_cnf_box=ans_dict_str)
            result.save()
            
            counter=0
            for q_id in selected_q_id_list:
                counter+=1
                quest=Question.objects.get(id=q_id)
                ans=request.POST['ans'+str(counter)]
                ansofcnfbox=AnsOfCnfBox(result_of_quiz=result, quest=quest, ans=ans)
                ansofcnfbox.save()
            request.session['player_id']=player.id
            #redirect('/cnfbx/result_view/'+str(quiz_id)+'/')
            return redirect(request.path, quiz_id=quiz_id)
        return render(request,'cb_create.html')

'''

def result_view(request, quiz_id):
    if 'user_type' in request.session:
        if request.session['user_type']=='creator' and 'user_id' in request.session:
            cnfbox=CnfBox.objects.filter(quiz_id=quiz_id).first()
            creator=cnfbox.creator
            u_id=request.session['user_id']
            
            if creator.id!=u_id:
                try:
                    raise ValueError('Correct Creator is not found.')
                except ValueError:
                    return render(request, 'error.html')
            selected_q_id_list=cnfbox.quest_selected_str.split(',')
            selected_q_list=dict()
            for q_id in selected_q_id_list:
                selected_q_list[q_id]=Question.objects.get(id=q_id).question.replace('<username>', creator.user_name)
            
            result_query=Result.objects.filter(cnf_box=cnfbox)
            #result_list=[res for res in result_query]
            result_list=list()
            #counter_res=0
            #counter_ans=0
            for res in result_query:
                #counter_res+=1
                res_item=dict()
                res_item['player_un']=res.player.user_name
                ans_query_of_res=AnsOfCnfBox.objects.filter(result_of_quiz=res)
                ans_of_res=dict()
                for quest_ans in ans_query_of_res:
                    ans_of_res[str(quest_ans.quest.id)]={ 'q_at_id' : selected_q_list[str(quest_ans.quest.id)], 'ans': quest_ans.ans}
                    '''
                    counter_ans+=0
                    quest_ans_item=dict()
                    quest_ans_item[str(quest_ans.quest.id)]=quest_ans.quest.id
                    quest_ans_item['ans'+str(quest_ans.quest.id)]=quest_ans.ans
                    ans_of_res['quest_ans_item'+str(counter_ans)]=quest_ans_item
                    '''
                    
                res_item['ans_of_res']=ans_of_res
                result_list.append(res_item)
            
            quiz_result={'creator_un':creator.user_name,'result_list':result_list, 'selected_q_list':selected_q_list}
            return render(request,'result.html', quiz_result)
        elif request.session['user_type']=='player' and 'user_id' in request.session:
            cnfbox=CnfBox.objects.filter(quiz_id=quiz_id).first()
            creator=cnfbox.creator
            
            selected_q_id_list=cnfbox.quest_selected_str.split(',')
            selected_q_list=dict()
            for q_id in selected_q_id_list:
                selected_q_list[q_id]=Question.objects.get(id=q_id).question.replace('<username>', creator.user_name)
            
            player_id=request.session['user_id']
            player=User.objects.get(id=player_id)
            result_query=Result.objects.filter(cnf_box=cnfbox, player=player)       
            #result_list=[res for res in result_query]
            
            result_list=list()
            #counter_res=0
            for res in result_query:
                #counter_res+=1
                res_item=dict()
                res_item['player_un']=res.player.user_name
                ans_query_of_res=AnsOfCnfBox.objects.filter(result_of_quiz=res)
                ans_of_res=dict()
                for quest_ans in ans_query_of_res:
                    ans_of_res[str(quest_ans.quest.id)]={ 'q_at_id' : selected_q_list[str(quest_ans.quest.id)], 'ans': quest_ans.ans}
                    '''
                    quest_ans_item=tuple()
                    quest_ans_item.append(quest_ans.quest.id)
                    quest_ans_item.append(quest_ans.ans)
                    ans_of_res.append(quest_ans_item)
                    '''
                res_item['ans_of_res']=ans_of_res
                result_list.append(res_item)
            
            quiz_result={'creator_un':creator.user_name,'result_list':result_list, 'selected_q_list':selected_q_list}
            
            return render(request,'result.html', quiz_result)
        return render(request,'cb_create.html')
    return render(request,'cb_create.html')

'''
#for testing JsonEncoder
class UserEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, User):
            return object.__dict__
        else:
            return json.JSONEncoder.default(self, object)


#for test
def result_testt(request, quiz_id):
    if request.method=='POST':
        #if 'ans1' in request.GET:
        st=""+quiz_id+": "
        for i in range(1,4):
            st+= request.POST['ans'+str(i)]
        return HttpResponse(st)
        #else:
        #    raise KeyError
    return HttpResponse('Nothing happen')
'''

def random_secure_string(stringLength=5):
    alphanumerics=string.ascii_letters+'123456789'
    secureStr = ''.join((secrets.choice(alphanumerics) for i in range(stringLength)))
    return secureStr
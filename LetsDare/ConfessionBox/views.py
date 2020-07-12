from django.shortcuts import render, redirect
from DareYou.models import Question
from ConfessionBox.models import User, CnfBox, AnsOfCnfBox, Result
import string
import secrets
from django.http.response import HttpResponse, JsonResponse,\
    HttpResponseNotFound
from rest_framework.views import APIView
from json.encoder import JSONEncoder
import json
from django.contrib import auth


# Create your views here.
def homepage(request):
    return redirect(cb_home)


def cb_home(request):
    return render(request, 'cb_home.html')


def contact_us(request):
    contact_email='sujeet.sharma2395@gmail.com'
    contact_fb='https://www.facebook.com/SujeetSharma4/'
    contact_insta='https://www.instagram.com/thesujitsharma/'
    return  render(request, 'contact_us.html',{'contact_email':contact_email, 'contact_fb':contact_fb,'contact_insta':contact_insta})

def about_us(request):
    return  render(request, 'about_us.html')


def cb_create(request):
    user_tracked={}
    un=""
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            un = User.objects.get(id=user_id).user_name
        except User.DoesNotExist:
            del request.session['user_id']
            un=""
    
    if un != "":
        is_creator=False
        if 'is_creator' in request.session:
            is_creator = request.session['is_creator']
               
        user_cnfbox_url='/cnfbx/user_cnfbox/'+str(user_id)+'/'
        
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
        
        selected_q_str=""
        if 'selected_q_str' in request.POST:
            selected_q_str=request.POST['selected_q_str']
        
        if un!="" and selected_q_str!="":
            selected_q_id_list=selected_q_str.split(',')
            selected_q_list=dict()
            for q_id in selected_q_id_list:
                selected_q_list[q_id]=q_dict[q_id]
            
            user=None
            if 'user_id' in request.session:    
                try:
                    user=User.objects.get(id=request.session['user_id'])
                except User.DoesNotExist:
                    del request.session['user_id']
                    user=None
            
            if user != None:
                if user.user_name != un:
                    User.objects.filter(id=request.session['user_id']).update(user_name=un)
            else:
                user=User(user_name=un)
                user.save()
            
            quiz_id=random_secure_string()
            cnf_box=CnfBox(quiz_id=quiz_id, creator=user, quest_selected_str=selected_q_str)
            cnf_box.save()
                           
            request.session['user_type']='creator'
            request.session['is_creator']=True
            request.session['user_id']=user.id
            
            return redirect(user_cnfbox, user_id=user.id)
    return render(request,'cb_create.html')


def user_cnfbox(request, user_id):
    creator=None
    if user_id > 0:
        try:
            creator=User.objects.get(id=user_id)
        except User.DoesNotExist:
            creator=None
            return render(request, 'error.html', {'error_msg':'User does not exit.'}, status=HttpResponseNotFound.status_code)
    
    if creator != None:
        request.session['user_type']='creator'
        request.session['is_creator']=True
        request.session['user_id']=user_id
            
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
            cnf_dare_url=httppart+request.get_host()+'/cnfbx/play_q/'+cnfbox.quiz_id+'/'
            result_view_url='/cnfbx/result_view/'+cnfbox.quiz_id+'/'
            cnfbox_items['cnf_dare_url']=cnf_dare_url
            cnfbox_items['result_view_url']=result_view_url
            cnfboxes.append(cnfbox_items)
        
        is_player=False
        if 'is_player' in request.session:
            is_player=request.session['is_player']
            
        return render(request, 'user_cnfboxes.html', {'cnfboxes':cnfboxes, 'un':creator.user_name, 'is_player': is_player, 'user_id': user_id})
    return render(request, 'cb_create.html')


def player(request, quiz_id):
    user_tracked={}
    un=""
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            un = User.objects.get(id=user_id).user_name
        except User.DoesNotExist:
            del request.session['user_id']
            un=""
    if un != "":
        is_player = False
        if 'is_player' in request.session:
            is_player=request.session['is_player']
        
        user_played_cnfbox_url='/cnfbx/user_played_cnfbox/'+str(user_id)+'/'
        user_tracked={'un': un, 'quiz_id':quiz_id, 'user_id': user_id, 'is_player': is_player, 'user_played_cnfbox_url': user_played_cnfbox_url}
        return render(request, 'player_un.html', user_tracked)
    return render(request, 'player_un.html',{'quiz_id':quiz_id})


def play_quiz(request, quiz_id):
    if request.method=='POST':
        player_un=request.POST['userName']
        cnfbox=CnfBox.objects.filter(quiz_id=quiz_id).first()
        if cnfbox==None:
            try:
                raise CnfBox.DoesNotExist
            except CnfBox.DoesNotExist:
                return render(request, 'error.html', {'error_msg':'Confession Box does not exit.'}, status=HttpResponseNotFound.status_code)
        if cnfbox != None:
            creator=cnfbox.creator
            creator_un=creator.user_name
            selected_q_id_list=cnfbox.quest_selected_str.split(',')
            selected_q_list=dict()
            for q_id in selected_q_id_list:
                selected_q_list[q_id]=Question.objects.get(id=q_id).question.replace('<username>', creator.user_name)
            
            cnf_player={'player_un':player_un, 'creator_un': creator_un, 'quiz_id':quiz_id, 'selected_q_list':selected_q_list}
            request.session['player_un']=player_un
            return render(request, 'play_quiz.html', cnf_player)
    return render(request, 'player_un.html',{'quiz_id':quiz_id})

def result(request, quiz_id):
    if request.method=='POST':
        player_un=request.session['player_un']
        player=None
        if 'user_id' in request.session:
            try:
                player=User.objects.get(id=request.session['user_id'])
            except User.DoesNotExist:
                del request.session['user_id']
                player=None
        
        if player != None:
            if player.user_name!=player_un:
                User.objects.filter(id=request.session['user_id']).update(user_name=player_un)
        else:
            player=User(user_name=player_un)
            player.save()
            
        cnfbox=CnfBox.objects.filter(quiz_id=quiz_id).first()
        if cnfbox==None:
            try:
                raise CnfBox.DoesNotExist
            except CnfBox.DoesNotExist:
                return render(request, 'error.html', {'error_msg':'Confession Box does not exit.'}, status=HttpResponseNotFound.status_code)
        
        if cnfbox != None:
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
    return render(request, 'player_un.html',{'quiz_id':quiz_id})


def user_played_cnfbox(request, user_id):
    if user_id>0:
        player=None
        try:
            player=User.objects.get(id=user_id)
        except User.DoesNotExist:
            player=None
            return render(request, 'error.html',{'error_msg': 'User does not exist.'}, status=HttpResponseNotFound.status_code)
        if player != None:
            
            request.session['user_type']='player'
            request.session['is_player']=True
            request.session['user_id']=user_id
            
            player_un=player.user_name
            result_query=Result.objects.filter(player=player)
            cnfboxes=list()
            unique_res=set()
            for res in result_query:
                if res.cnf_box.id not in unique_res:
                        unique_res.add(res.cnf_box.id)
                else:
                    continue
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
                result_view_url='/cnfbx/result_view/'+cnfbox.quiz_id+'/'
                cnfbox_items['result_view_url']=result_view_url
                cnfboxes.append(cnfbox_items)
            
            is_creator=False
            if 'is_creator' in request.session:
                is_creator=request.session['is_creator']
            
            return render(request, 'user_played_cnfboxes.html', {'cnfboxes':cnfboxes, 'player_un':player_un, 'is_creator': is_creator, 'user_id': user_id})
    return render(request, 'cb_create.html')


def result_view(request, quiz_id):
    if 'user_type' in request.session:
        if request.session['user_type']=='creator' and 'user_id' in request.session:
            cnfbox=CnfBox.objects.filter(quiz_id=quiz_id).first()
            if cnfbox==None:
                try:
                    raise CnfBox.DoesNotExist
                except CnfBox.DoesNotExist:
                    return render(request, 'error.html', {'error_msg':'Confession Box does not exit.'}, status=HttpResponseNotFound.status_code)
            if cnfbox != None:
                creator=cnfbox.creator
                u_id=request.session['user_id']
                
                if creator.id!=u_id:
                    try:
                        raise ValueError('Correct Creator is not found.')
                    except ValueError as ex:
                        return render(request, 'error.html', {'error_msg':ex}, status=HttpResponseNotFound.status_code)
                else:
                    selected_q_id_list=cnfbox.quest_selected_str.split(',')
                    selected_q_list=dict()
                    for q_id in selected_q_id_list:
                        selected_q_list[q_id]=Question.objects.get(id=q_id).question.replace('<username>', creator.user_name)
                    
                    result_query=Result.objects.filter(cnf_box=cnfbox)
                    result_list=list()
                    for res in result_query:
                        res_item=dict()
                        res_item['player_un']=res.player.user_name
                        ans_query_of_res=AnsOfCnfBox.objects.filter(result_of_quiz=res)
                        ans_of_res=dict()
                        for quest_ans in ans_query_of_res:
                            ans_of_res[str(quest_ans.quest.id)]={ 'q_at_id' : selected_q_list[str(quest_ans.quest.id)], 'ans': quest_ans.ans}
                        res_item['ans_of_res']=ans_of_res
                        result_list.append(res_item)
                    
                    quiz_result={'creator_un':creator.user_name,'result_list':result_list, 'selected_q_list':selected_q_list}
                    return render(request,'result.html', quiz_result)
        elif request.session['user_type']=='player' and 'user_id' in request.session:
            
            cnfbox=CnfBox.objects.filter(quiz_id=quiz_id).first()
            if cnfbox==None:
                try:
                    raise CnfBox.DoesNotExist
                except CnfBox.DoesNotExist:
                    return render(request, 'error.html', {'error_msg':'Confession Box does not exit.'}, status=HttpResponseNotFound.status_code)
            if cnfbox!= None:
                creator=cnfbox.creator
                
                selected_q_id_list=cnfbox.quest_selected_str.split(',')
                selected_q_list=dict()
                for q_id in selected_q_id_list:
                    selected_q_list[q_id]=Question.objects.get(id=q_id).question.replace('<username>', creator.user_name)
                
                player_id=request.session['user_id']
                player=User.objects.get(id=player_id)
                result_query=Result.objects.filter(cnf_box=cnfbox, player=player)       
                result_list=list()
                for res in result_query:
                    res_item=dict()
                    res_item['player_un']=res.player.user_name
                    ans_query_of_res=AnsOfCnfBox.objects.filter(result_of_quiz=res)
                    ans_of_res=dict()
                    for quest_ans in ans_query_of_res:
                        ans_of_res[str(quest_ans.quest.id)]={ 'q_at_id' : selected_q_list[str(quest_ans.quest.id)], 'ans': quest_ans.ans}
                    res_item['ans_of_res']=ans_of_res
                    result_list.append(res_item)
                
                quiz_result={'creator_un':creator.user_name,'result_list':result_list, 'selected_q_list':selected_q_list}
                
                return render(request,'result.html', quiz_result)
        return render(request,'cb_create.html')
    return render(request,'cb_create.html')


def random_secure_string(stringLength=5):
    alphanumerics=string.ascii_letters+'123456789'
    secureStr = ''.join((secrets.choice(alphanumerics) for i in range(stringLength)))
    return secureStr
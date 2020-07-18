from django.shortcuts import get_object_or_404, render
from django.template.context_processors import request
from rest_framework import status, generics, mixins, viewsets
from DareYou.serializers import QuestionSerializersModel, DareSharedSerializers
from rest_framework.authentication import TokenAuthentication,\
    SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from DareYou.models import Question, DareShared
from requests.sessions import session
from django.http.response import HttpResponse


def home(request):
    return render(request, 'index.html')

def create(request):
    return render(request, 'create.html')

def select_un(request):
    if request.method=='POST':
        un=request.POST['userName']
        if un!="":
            q_list=Question.objects.all()
            q_dict=dict()
            for q in q_list:
                q_dict[str(q.id)]=q.question.replace('<username>', un)
            dared={'un':un,'q_dict':q_dict}
            request.session['dared']=dared
            return render(request, 'select.html',dared)
    return render(request, 'create.html')

def select_q(request):
    if request.method=='POST':
        if 'dared' in request.session:
            dared=request.session['dared']
            q_dict=dared['q_dict']
            un=dared['un']
        selected_q_str=request.POST['selected_q_str']
        if un!="" and selected_q_str!="":
            selected_q_id_list=selected_q_str.split(',')
            selected_q_list=dict()
            for q_id in selected_q_id_list:
                selected_q_list[q_id]=q_dict[q_id]
            dareshared=DareShared()
            dareshared.creator_name=un
            dareshared.ques_selected_str=selected_q_str
            dareshared.save()
            #dare_url='127.0.0.1:8000/dareyou/dareshared/'+str(dareshared.id)
            httppart='https://'
            if request.get_host()=='127.0.0.1:8000':
                httppart='http://'
            else:
                httppart='https://'
            dare_url=httppart+request.get_host()+'/dareyou/dareshared/'+str(dareshared.id)
            dared_q={'un':un,'selected_q_list':selected_q_list,'dare_url':dare_url}
            return render(request, 'sharedare.html',dared_q)
    return render(request,'/')

def playdareview(request,id):
    try:
        dareshared = DareShared.objects.get(id=id)
        if dareshared:
            un=dareshared.creator_name
            selected_q_id_list=dareshared.ques_selected_str.split(',')
            selected_q_list=dict()
            for q_id in selected_q_id_list:
                selected_q_list[q_id]=Question.objects.get(id=q_id).question.replace('<username>', un)
            dared_q={'un':un,'selected_q_list':selected_q_list}
            return render(request, 'playdare.html',dared_q)
    except (DareShared.DoesNotExist, KeyError) as e:
        return render(request, 'error.html', {'error_msg':e})

# Create your views here.
class QuestionsGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=QuestionSerializersModel
    queryset=Question.objects.all()
    lookup_field='id'
    authentication_classes=[SessionAuthentication, BasicAuthentication]
    #authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        return self.list(request)
    def post(self,request):
        return self.create(request)
    
    def put(self,request,id):
        return self.update(request,id)
    
    def delete(self, request, id):
        return self.destroy(request, id)
    
class DareSharedGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=DareSharedSerializers
    queryset=DareShared.objects.all()
    lookup_field='id'
    authentication_classes=[SessionAuthentication, BasicAuthentication]
    #authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        return self.list(request)
    def post(self,request):
        return self.create(request)
    
    def put(self,request,id):
        return self.update(request, id)
    
    def delete(self, request, id):
        return self.destroy(request, id)

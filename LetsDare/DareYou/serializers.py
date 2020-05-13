from rest_framework import serializers
from DareYou.models import Question, DareShared

class QuestionSerializersModel(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=['id', 'type','question']
        #fields = '__all__'
    def str(self):
        return str(self.id+': '+self.type)

class QuestionSerializers(serializers.Serializer):
    type = serializers.CharField(max_length=100)
    question = serializers.CharField(max_length=250)
    
    def create(self, validated_data):
        return Question.objects.create(validated_data)
    
    def update(self, instance, validated_data):
        instance.type=validated_data.get('type',instance.type)
        instance.question=validated_data.get('question',instance.question)
        instance.save()
        return instance

class DareSharedSerializers(serializers.Serializer):    
    creator_name=serializers.CharField(max_length=100)
    ques_selected_str=serializers.CharField(max_length=100)
    
    def create(self, validated_data):
        return DareShared.objects.create(validated_data)
    def update(self, instance, validated_data):
        instance.creator_name=validated_data.get('creator_name', instance.creator_name)
        instance.ques_selected_str=validated_data.get('question', instance.question)
        instance.save()
        return instance

"""
In [1]: from accounts.models import Post

In [2]: from accounts.serializers import PostSerializersModel

In [3]: p=Post.objects.get(pk=1)

In [4]: s=PostSerializersModel(p)

In [5]: print(repr(s))
PostSerializersModel(<Post: Post object (1)>):
    title = CharField(max_length=100)
    description = CharField(style={'base_template': 'textarea.html'})
    published_date = DateField()
    location = CharField(max_length=100)



*************

In [1]: from accounts.models import Post

In [2]: from accounts.serializers import PostSerializersModel

In [3]: p=Post.objects.get(pk=1)

In [4]: s=PostSerializersModel(p)

In [5]: print(repr(s))
PostSerializersModel(<Post: Post object (1)>):
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=100)
    description = CharField(style={'base_template': 'textarea.html'})
    post_image = ImageField(max_length=100)
    published_date = DateField()
    tags = CharField(max_length=100)
    location = CharField(max_length=100)
    posted_by = PrimaryKeyRelatedField(queryset=User.objects.all())

In [6]:
"""
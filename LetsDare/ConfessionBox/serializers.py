from rest_framework import serializers
from ConfessionBox.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        #fields=['id', 'title','description','published_date','location','posted_by']
        fields = '__all__'
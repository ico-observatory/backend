from rest_framework import serializers
from .models import Query, Version, Worker, QueryFile, HandleVersion


class QuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Query
        fields = '__all__'
    
    
class VersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Version
        fields = '__all__'
        
    
class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = '__all__'
        
        
class QueryFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = QueryFile
        fields = '__all__'
        
        
class HandleVersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = HandleVersion
        fields = '__all__'

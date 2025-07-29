from rest_framework import serializers

class CityListAPIViewSerializer(serializers.Serializer):
    city = serializers.CharField()
    total_searches = serializers.IntegerField()

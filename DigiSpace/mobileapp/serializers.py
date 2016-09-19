from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required= True)
    password = serializers.CharField(max_length=20, required= True)

class AdvertMapListSerializer(serializers.Serializer):
    city_id = serializers.CharField(required= True)
    consumer_latitude = serializers.CharField(required= True)
    consumer_longitude = serializers.CharField(required= True)
    radius = serializers.CharField(required= True)

class PostReviewSerializer(serializers.Serializer):
    advert_id = serializers.CharField(required= True)
    user_id = serializers.CharField(required= True)
    ratings = serializers.CharField(required= True)
    review = serializers.CharField(required= True)
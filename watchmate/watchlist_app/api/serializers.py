from django.db.models import fields
from rest_framework import serializers
from watchlist_app.models import Review, WatchList, StreamPlatform

# Using ModelSerializer

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ['watchlist']


class WatchListSerializer(serializers.ModelSerializer):
    # name_length = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = WatchList
        fields = '__all__'


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = '__all__'

    
    
    # def get_name_length(self, object):
    #     length = len(object.name)
    #     return length



    # def validate_name(self, value):
    #     if len(value) < 3:
    #         raise serializers.ValidationError('Name should be at least 3 characters')
    #     return value

    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError(' Name and description should be different')
    #     return data


# Normal Serializer Class

# def name_length(name):
#     if len(name) < 3:
#         raise serializers.ValidationError(' Name should be more than 3 characters')

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate_name(self, value):
#         if len(value) < 3:
#             raise serializers.ValidationError('Name should be at least 3 characters')
#         return value

    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError(' Name and description should be different')
    #     return data
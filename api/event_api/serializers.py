from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.text import slugify
from event.models import Event, Event_User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class EventUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Event_User
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    event_user = EventUserSerializer(source='event_user_set', many=True, read_only=True)
    user = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Event
        fields = (
            'slug','name', 'cover_picture', 'description',
            'start_date', 'end_date', 'available_seats',
            'price', 'status', 'event_user', 'user'
        )
        extra_kwargs = {
            'cover_picture': {'required': False},
            'slug': {'required': False},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        event = Event(**validated_data)
        event.save() 
        
        event.user.add(user)  

        slug = slugify(event.name)
        unique_slug = slug
        num = 1
        while Event.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1

        event.slug = unique_slug
        event.save()

        return event

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.cover_picture = validated_data.get('cover_picture', instance.cover_picture)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.available_seats = validated_data.get('available_seats', instance.available_seats)
        instance.price = validated_data.get('price', instance.price)
        instance.status = validated_data.get('status', instance.status)
        
        if 'name' in validated_data:
            slug = slugify(validated_data['name'])
            if instance.slug != slug:
                unique_slug = slug
                num = 1
                while Event.objects.filter(slug=unique_slug).exists():
                    unique_slug = f'{slug}-{num}'
                    num += 1
                instance.slug = unique_slug
        
        instance.save()

        if 'user' in validated_data:
            user_ids = [user_data['id'] for user_data in validated_data['user']]
            instance.user.set(User.objects.filter(id__in=user_ids))
        
        instance.save()
        return instance

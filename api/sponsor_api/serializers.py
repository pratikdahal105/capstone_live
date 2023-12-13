from rest_framework import serializers
from django.utils.text import slugify
from sponsor.models import Sponsor
from event.models import Event

class EventSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        request = self.context.get('request', None)
        if request:
            slug = data
            try:
                event = Event.objects.get(slug=slug, user=request.user)
                return event
            except Event.DoesNotExist:
                raise serializers.ValidationError(f"Event with slug '{slug}' does not exist.")
        else:
            raise serializers.ValidationError("Request is not available in the context.")

class SponsorSerializer(serializers.ModelSerializer):
    event = EventSlugRelatedField(
        queryset=Event.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Sponsor
        fields = ('event', 'slug', 'name', 'logo', 'description', 'amount_sponsored', 'sponsor_level')

    def validate_name(self, value):
        if 'name' in self.initial_data and self.instance and self.instance.name != value:
            new_slug = slugify(value)
            if Sponsor.objects.filter(slug=new_slug).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A sponsor with that name already exists.")
        return value

    def create(self, validated_data):
        name = validated_data.get('name')
        slug = slugify(name)
        unique_slug = slug
        num = 1
        while Sponsor.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        validated_data['slug'] = unique_slug
        return Sponsor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        if name and name != instance.name:
            slug = slugify(name)
            unique_slug = slug
            num = 1
            while Sponsor.objects.filter(slug=unique_slug).exclude(pk=instance.pk).exists():
                unique_slug = f'{slug}-{num}'
                num += 1
            instance.slug = unique_slug
        instance.name = validated_data.get('name', instance.name)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.description = validated_data.get('description', instance.description)
        instance.amount_sponsored = validated_data.get('amount_sponsored', instance.amount_sponsored)
        instance.sponsor_level = validated_data.get('sponsor_level', instance.sponsor_level)
        instance.save()
        return instance

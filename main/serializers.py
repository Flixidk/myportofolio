from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Skill

class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category",
            "started_at", "ended_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):    
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

class SkillSerializer(serializers.ModelSerializer):
    endorse_count = serializers.SerializerMethodField()
    is_endorsed = serializers.SerializerMethodField()
    endorsed_by_names = serializers.SerializerMethodField()

    class Meta:
            model = Skill
            fields = [
                "id", "title", "description", "category", "icon_path",
                "endorse_count", "is_endorsed", "endorsed_by_names",
            ]
            read_only_fields = ["id"]

    def validate_title(self, value):    
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama skill tidak boleh hanya berisi tag HTML.")
        return value
    
    def validate_description(self, value):
        return strip_tags(value)

    def validate_icon_path(self, value):
        return strip_tags(value)

    def get_endorse_count(self, obj):
        return obj.endorsed_by.count()

    def get_is_endorsed(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.endorsed_by.all()

    def get_endorsed_by_names(self, obj):
        return ", ".join(user.username for user in obj.endorsed_by.all())
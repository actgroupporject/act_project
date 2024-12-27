from rest_framework import serializers

from .models import Actor, ActorImage, ActorVideo, Application, Recruit


class RecruitSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Recruit
        fields = "__all__"

    def validate_closing_at(self, value):
        if value <= self.initial_data["post_at"]:
            raise serializers.ValidationError("Closing date must be after posting date.")
        return value


class ApplicationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source="actor.user.username")

    class Meta:
        model = Application
        fields = "__all__"


class ActorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActorImage
        fields = "__all__"


class ActorVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActorVideo
        fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):
    images = ActorImageSerializer(many=True, read_only=True)
    videos = ActorVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = "__all__"

    def validate_stature(self, value):
        if value < 0 or value > 300:
            raise serializers.ValidationError("Invalid height.")
        return value

    def validate_weight(self, value):
        if value < 0 or value > 500:
            raise serializers.ValidationError("Invalid weight.")
        return value

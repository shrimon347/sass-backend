# your_app/serializers.py
from rest_framework import serializers
from .models import CodeGenrator, Conversation,ContentGenrator

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['prompt']

class CodeGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeGenrator
        fields = ['prompt']
class ContentGeneratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentGenrator
        fields = ['prompt']




class ImageGenerationSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=255)
    # amount = serializers.IntegerField(default=1, min_value=1, max_value=10)
    # resolution = serializers.ChoiceField(
    #     choices=[("256x256", "256x256"), ("512x512", "512x512"), ("1024x1024", "1024x1024")],
    #     default="1024x1024"
    # )
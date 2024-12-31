# your_app/models.py
from django.db import models

class Conversation(models.Model):
    user_id = models.CharField(max_length=255)  # Store user ID from Clerk
    prompt = models.TextField()  # User's prompt
    response = models.TextField()  # Response from OpenAI
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f'Conversation({self.user_id}, {self.prompt}, {self.response})'

class CodeGenrator(models.Model):
    user_id = models.CharField(max_length=255)  # Store user ID from Clerk
    prompt = models.TextField()  # User's prompt
    response = models.TextField()  # Response from OpenAI
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f'CodeGenerator({self.user_id}, {self.prompt}, {self.response})'
    
    
class ContentGenrator(models.Model):
    user_id = models.CharField(max_length=255)  # Store user ID from Clerk
    prompt = models.TextField()  # User's prompt
    response = models.TextField()  # Response from OpenAI
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f'ContentGenerator({self.user_id}, {self.prompt}, {self.response})'
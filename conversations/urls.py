from django.urls import path
from .views import ConversationView,CodeView,GenerateImageView,ContentView

urlpatterns = [
    path('conversations/', ConversationView.as_view(), name='conversation'),
    path('code/', CodeView.as_view(), name='codegenerator'),
    path('image/', GenerateImageView.as_view(), name='imagegenerator'),
    path('content/', ContentView.as_view(), name='contentgenrator'),
]

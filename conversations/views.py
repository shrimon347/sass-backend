
from django.conf import settings
from g4f.client import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContentGenrator, Conversation
from .serializers import (CodeGeneratorSerializer, ContentGeneratorSerializer,
                          ConversationSerializer, ImageGenerationSerializer)

client = Client()

class ConversationView(APIView):
    def post(self, request):
        user_id = request.user_id
        if not user_id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data['prompt']

            try:
                # Use the ChatCompletion method for gpt-3.5-turbo
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a conversational assistant."},
                        {"role": "user", "content": message},
                    ],
                    max_tokens=150,
                    temperature=0.7,
                )
                answer = response.choices[0].message.content.strip()

                # Save the conversation to the database
                Conversation.objects.create(
                    user_id=user_id,
                    prompt=message,
                    response=answer,
                )

                return Response({
                    "role": "assistant",
                    "content": answer
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeView(APIView):
    def post(self, request):
        user_id = request.user_id
        if not user_id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CodeGeneratorSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data['prompt']

            try:
                # Use the ChatCompletion method for gpt-3.5-turbo
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": (
            "You are an advanced code generator specifically designed to deliver clear and efficient code snippets in Markdown format. "
            "For every code snippet you generate, include comments within the code to explain each section and its purpose. "
            "Additionally, provide a Markdown list below the code snippet summarizing the key points of the implementation and "
            "the reasoning behind the chosen approach. Focus on the following guidelines: "
            "- **Clarity:** Ensure the code is easy to read and understand. "
            "- **Functionality:** The code should work correctly for the given task. "
            "- **Best Practices:** Follow coding best practices to ensure quality. "
            "Your responses should contain only the essential code along with the explanations, without any unnecessary details."
        )},
                        {"role": "user", "content": message},
                    ],
                    max_tokens=150,
                    temperature=0.7,
                )
                answer = response.choices[0].message.content.strip()

                # Save the conversation to the database
                Conversation.objects.create(
                    user_id=user_id,
                    prompt=message,
                    response=answer,
                )

                return Response({
                    "role": "assistant",
                    "content": answer
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentView(APIView):
    def post(self, request):
        user_id = request.user_id
        if not user_id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ContentGeneratorSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data['prompt']

            # Check for user's latest response for continuity
            # latest_conversation = (
            #     ContentGenrator.objects.filter(user_id=user_id)
            #     .order_by('-created_at')
            #     .first()
            # )

            # Analyze the prompt to detect platform or content type
            if any(keyword in prompt.lower() for keyword in ["instagram", "twitter", "facebook", "linkedin"]):
                platform = "specific"  # Indicates it's for a specific platform based on prompt content
            else:
                platform = "general"  # Defaults to general if no platform is specified

            content_type = "idea and script" if "idea" in prompt.lower() or "script" in prompt.lower() else "idea"

            # Construct the message
            message = f"Generate {content_type} for {platform} based on: {prompt}"
            # if latest_conversation:
            #     message += f" Consider previous content: {latest_conversation.response}"

            try:
                # Call AI to generate the response
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
    {
        "role": "system",
        "content":(
            "### System Message for Social Media Content Generation\n\n"
            "1. **Role and Focus:**\n"
            "   - 'You are a creative content generator specializing in social media platforms.'\n\n"
            "2. **Platform Customization:**\n"
            "   - 'When the user specifies a platform (e.g., Instagram, Twitter, Facebook, LinkedIn), adjust the content style, tone, and format accordingly.'\n\n"
            "3. **General Use Content:**\n"
            "   - 'If no platform is mentioned, provide a versatile content idea and script suitable for general use.'\n\n"
            "4. **Creative Components:**\n"
            "   - 'Generate fresh ideas, engaging captions, and, if appropriate, suggest hashtags, calls-to-action, or attention-grabbing intros.'\n\n"
            "5. **Content Style:**\n"
            "   - 'Keep scripts concise, relatable, and tailored to audience engagement.'\n\n"
            "### Hashtag Suggestions\n"
            "- Include relevant hashtags based on the platform and content type (e.g., #Inspiration, #MondayMotivation, #SocialMediaTips).\n\n"
            "### Information Part\n"
            "- **Purpose:** Deliver engaging and platform-specific content that enhances user engagement.\n"
            "- **Guidelines for Engagement:** Adapt style and tone for platform needs, include a relatable tone, and make use of actionable captions or CTAs when necessary."
        )
    },
    {
        "role": "user",
        "content": message,
    },
],
                    max_tokens=500,
                    temperature=0.7,
                )
                answer = response.choices[0].message.content.strip()

                # Save conversation history
                Conversation.objects.create(
                    user_id=user_id,
                    prompt=prompt,
                    response=answer,
                )

                return Response({
                    "content": answer
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateImageView(APIView):
    
    def post(self, request):
        user_id = request.user_id
        if not user_id:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = ImageGenerationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 

        # Extract validated data
        validated_data = serializer.validated_data
        prompt = validated_data["prompt"]
        # amount = validated_data["amount"]
        # resolution = validated_data["resolution"] 
        # try:
        #     width, height = map(int, resolution.split("X"))
        # except ValueError:
        #     return Response({"error": "Invalid resolution format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Generate images using the specified model
            response = client.images.generate(
                model="flux",
                prompt=prompt,
                # n=amount,
                # size = resolution 
                
            )
            # print(response.data)
            image_urls = [image.url for image in response.data]

            return Response(image_urls, status=status.HTTP_200_OK)

        except ValueError as ve:
            return Response(
                {
                    "error": "Invalid model or parameters",
                    "details": str(ve)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "error": "Failed to generate images",
                    "details": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

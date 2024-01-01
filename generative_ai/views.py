from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from openai import OpenAI
import asyncio
from openai import AsyncOpenAI
from rest_framework.permissions import IsAuthenticated,AllowAny
import requests
from django.http import JsonResponse
from decouple import config


# openai_api_key = config("OPENAI_API_KEY")

openAI_client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ArticleContentcreationByOpenai(APIView):
    
    permission_classes = (IsAuthenticated,)
    def post(self,request):

        try:
            # topic = self.request.query_params.get('topic')
            topic = self.request.data['topic']
            

            prompt = f"Create a essay about {topic}.Include Main Points. Limit with 100 words.Respond Only to valid tech Topics which is given.Do not respond to other topics.Response should be bullet point format."

            completion = openAI_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            return Response(completion.choices[0].message, status=status.HTTP_200_OK)
        
        except Exception as e:
            import traceback
            traceback_str = traceback.format_exc()
            print(f"Error in content generation: {e}\n{traceback_str}")
            return Response(f"{e}:error in content generation",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


def get_technology_news(request):
    api_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "in",
        "category": "technology",
        "apiKey": "779335093dc943fc916cff1ac2af4308",
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
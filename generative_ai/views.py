from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from openai import OpenAI
import asyncio
from openai import AsyncOpenAI
from rest_framework.permissions import IsAuthenticated,AllowAny

openAI_client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ArticleContentcreationByOpenai(APIView):
    
   def post(self,request):
        permission_classes = (IsAuthenticated,)

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

            return Response(f"{e}:error in content generation",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


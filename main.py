import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from typing import Optional, Dict
from openai import OpenAI
import httpx


OPENAI_API_KEY ="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"

OPENAI_BASE_URL = "https://openrouter.ai/api/v1"

# for logging purpose it will log all the information in app.log file,
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


FastAPI_URL = "http://127.0.0.1:8000"

# Initialize FastAPI app
app = FastAPI(
    title="Explanation on topic based on certain context API",
    description="API for explanation on topic based on certain context",
    version="1.0.0"
)

class Request(BaseModel):
    topic: str
    subject: str
    grade_level: int
    language: str
    custom_prompt:List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Artificial Intelligence",
                "subject": "Science",
                "grade_level": 12,
                "language": "English",
                "custom_prompt": ["Provide an explanation for the topic Artificial Intelligence in English language."]
            }
        }


class Response(BaseModel):
    explanations: List[str]
    grade_level: int
    timestamp: str


class ResponseGenerator:
    def __init__(
        self, 
        api_key: str, 
        base_url: str = "https://openrouter.ai/api/v1",
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

    def generate_response(self, prompt:str,topic: str, grade_level: str, language:str, model: str = "openai/gpt-4o-mini") -> Optional[str]:
        """
        Generate structured and engaging explnations based on subject, about the topic for the specified grade level,        """
        try:
            print(prompt)


            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert educator who provides explanation tailored to students based on specified grade levels. 
                        Each explanation should be engaging, structured, and appropriate for the given grade level in their specified language."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return None

def generate_explanation(topic: str,idx:int ,custom_prompt:list,subject:str ,grade_level: str,language:str) -> str:
    """
    Process the topic and grade level to generate structured explanation
    
    Args:
        topic (str): The topic to be explained
        subject (str): The subject of the topic
        grade_level (str): The grade level of the student
        api_key (str): API key for OpenRouter
        
    Returns:
        str: Structured explanations
    """
    # prompts = [f"\n\nGrade Level: {grade_level}\nSubject: {subject} \nTopic: {topic} \n\nProvide explanation for given topic of {topic} from subject {subject} and for grade level {grade_level} in {language} language.",
    #            f"\n\nGrade Level: {grade_level}\nSubject: {subject} \nTopic: {topic} \n\nProvide an elaborate curriculum equations with real-life examples,(if available) for topic {topic} from subject {subject} and grade level {grade_level} in {language} language.",
    #            f"\n\nGrade Level: {grade_level}\nSubject: {subject} \nTopic: {topic} \n\nProvide an elaborate different use cases for topic {topic} from subject {subject} and grade level {grade_level} at certain fields and in {language} language.",
    #            f"\n\nGrade Level: {grade_level}\nSubject: {subject} \nTopic: {topic} \n\nProvide most probable objective-type questions along with answers related to the topic (5 questions, tough and medium range, closely aligned with the National Testing Agency’s (NTA) approach for NEET exam questions) for topic {topic} from subject {subject} and grade level {grade_level} and in {language} language.",
    #            f"\n\nGrade Level: {grade_level}\nSubject: {subject} \nTopic: {topic} \n\nProvide all questions and answers from the past 10 years of NEET question papers related to the topic for topic {topic}from subject {subject} and grade level {grade_level} at certain fields and in {language} language."]
    prompts=[]
    prompts =[f"\n\nGrade Level: {grade_level}\nSubject: {subject} \nTopic: {topic} \n"+i for i in custom_prompt]
    
    response_gen = ResponseGenerator(
        api_key=OPENAI_API_KEY
    )

    if idx==None:
        out=[]
        for prompt in prompts:
            out+=[response_gen.generate_response(prompt,topic, grade_level , language)]
        return out
        
    return response_gen.generate_response(prompts[idx],topic, grade_level , language) or ""



@app.post("/generate-explanations", response_model=Response)
async def generate_explanations(request: Request):
    try:
        logger.info(f"Generating explanation on topic: {request.topic},subject: {request.subject}, grade level: {request.grade_level}, language: {request.language}")


        if not OPENAI_API_KEY:
            raise HTTPException(status_code=500, detail="OpenAI API key is not provided")
        
        texts = generate_explanation(topic=request.topic, idx=None, custom_prompt=request.custom_prompt ,subject=request.subject, grade_level=request.grade_level,language=request.language)

        return Response(
            explanations=texts,
            grade_level=request.grade_level,
            timestamp=datetime.now().isoformat(),
        )
    
    except Exception as e:
        logger.error(f"Error providing explanations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error providing explanations: {str(e)}")  


        






"""
AI Processor
OpenAI API használata adatok feldolgozásához
"""

import openai
import logging
import json
from typing import Dict, List, Optional
from ..config.settings import settings

logger = logging.getLogger(__name__)

# OpenAI API key beállítása
openai.api_key = settings.OPENAI_API_KEY


class AIProcessor:
    """AI feldolgozó osztály OpenAI használatával"""
    
    def __init__(self):
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE
    
    def normalize_salary(self, salary_text: str) -> Dict:
        """
        Fizetési információk normalizálása AI segítségével
        
        Példa:
        Input: "450-650 ezer Ft havonta"
        Output: {"min": 450000, "max": 650000, "currency": "HUF", "period": "monthly"}
        """
        if not salary_text or not openai.api_key:
            return {"min": None, "max": None, "currency": "HUF", "period": "monthly"}
        
        prompt = f"""
Normalize this Hungarian job salary information to structured data:

Input: "{salary_text}"

Output format (JSON):
{{
    "min": <minimum salary as integer>,
    "max": <maximum salary as integer>,
    "currency": "HUF",
    "period": "monthly" or "yearly" or "hourly"
}}

Examples:
- "450-650 ezer Ft/hó" -> {{"min": 450000, "max": 650000, "currency": "HUF", "period": "monthly"}}
- "6-8 millió Ft/év" -> {{"min": 6000000, "max": 8000000, "currency": "HUF", "period": "yearly"}}
- "2500 Ft/óra" -> {{"min": 2500, "max": 2500, "currency": "HUF", "period": "hourly"}}

Only return the JSON, nothing else.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data normalization assistant for Hungarian job salary information."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            result = response.choices[0].message.content.strip()
            return json.loads(result)
            
        except Exception as e:
            logger.error(f"Error normalizing salary with AI: {e}")
            return {"min": None, "max": None, "currency": "HUF", "period": "monthly"}
    
    def categorize_job(self, title: str, description: str) -> str:
        """
        Munkakör kategorizálása AI segítségével
        
        Kategóriák: IT, Engineering, Sales, Marketing, HR, Finance, Operations, Legal, Healthcare, Education, Other
        """
        if not title or not openai.api_key:
            return "Other"
        
        prompt = f"""
Categorize this Hungarian job posting into ONE of these categories:
- IT (Information Technology, Software Development, DevOps)
- Engineering (Mechanical, Electrical, Civil Engineering)
- Sales (Sales Representative, Account Manager)
- Marketing (Digital Marketing, Content Marketing, SEO)
- HR (Human Resources, Recruitment)
- Finance (Accounting, Financial Analysis, Banking)
- Operations (Logistics, Supply Chain, Production)
- Legal (Lawyer, Legal Counsel)
- Healthcare (Doctor, Nurse, Medical)
- Education (Teacher, Trainer)
- Other

Job Title: "{title}"
Description: "{description[:500]}"

Output: Only the category name, nothing else.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a job categorization assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            category = response.choices[0].message.content.strip()
            return category
            
        except Exception as e:
            logger.error(f"Error categorizing job with AI: {e}")
            return "Other"
    
    def extract_skills(self, description: str) -> List[str]:
        """
        Készségek kivonatolása állásleírásból AI segítségével
        """
        if not description or not openai.api_key:
            return []
        
        prompt = f"""
Extract required technical and soft skills from this Hungarian job description.

Job Description:
"{description[:1500]}"

Output format: JSON array of skills
Example: ["Python", "SQL", "Communication", "Problem Solving", "Git"]

Return only the JSON array, nothing else.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a skill extraction assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            result = response.choices[0].message.content.strip()
            skills = json.loads(result)
            return skills if isinstance(skills, list) else []
            
        except Exception as e:
            logger.error(f"Error extracting skills with AI: {e}")
            return []
    
    def determine_experience_level(self, title: str, description: str) -> str:
        """
        Tapasztalati szint meghatározása AI segítségével
        
        Szintek: junior, medior, senior, lead, executive
        """
        if not title or not openai.api_key:
            return "medior"
        
        prompt = f"""
Determine the experience level for this Hungarian job posting.

Levels: junior, medior, senior, lead, executive

Job Title: "{title}"
Description: "{description[:500]}"

Output: Only the level name, nothing else.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a job experience level classifier."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=20
            )
            
            level = response.choices[0].message.content.strip().lower()
            return level
            
        except Exception as e:
            logger.error(f"Error determining experience level with AI: {e}")
            return "medior"
    
    def enrich_job_data(self, job_data: Dict) -> Dict:
        """
        Állás adatok dúsítása AI segítségével
        Kombinálja az összes AI funkciót
        """
        enriched = job_data.copy()
        
        # Fizetés normalizálás
        if job_data.get("salary_text"):
            salary_info = self.normalize_salary(job_data["salary_text"])
            enriched.update(salary_info)
        
        # Kategorizálás
        if job_data.get("title") and job_data.get("description"):
            enriched["category"] = self.categorize_job(
                job_data["title"],
                job_data["description"]
            )
        
        # Készségek
        if job_data.get("description"):
            enriched["skills"] = self.extract_skills(job_data["description"])
        
        # Tapasztalati szint
        if job_data.get("title") and job_data.get("description"):
            enriched["experience_level"] = self.determine_experience_level(
                job_data["title"],
                job_data["description"]
            )
        
        return enriched


# Singleton instance
ai_processor = AIProcessor()

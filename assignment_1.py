import re
import os
import json
from PyPDF2 import PdfReader
from docx import Document

class EnglishResumeParser:
    def __init__(self):
        pass
    
    def parse_pdf(self, file_path):
        text = ""
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def parse_word(self, file_path):
        doc = Document(file_path)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        return text
    
    def parse_name(self, text):
        name_pattern = re.compile(r'([A-Z][a-z]+(?: [A-Z][a-z]+)?)')
        match = name_pattern.search(text)
        if match:
            name = match.group(0)
        else:
            name = None
        return name
    
    def parse_email(self, text):
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        match = email_pattern.search(text)
        if match:
            email = match.group(0)
        else:
            email = None
        return email
    
    def parse_phone(self, text):
        phone_pattern = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        match = phone_pattern.search(text)
        if match:
            phone = match.group(0)
        else:
            phone = None
        return phone
    
    def parse_summary(self, text):
        # Extracting summary based on common patterns
        summary = {
            "benefits": "",
            "objective": "",
            "description": "",
            "notice_period": "",
            "current_salary": ""
        }
        # Implement logic to extract summary information
        # For example:
        # summary['objective'] = "Seeking a challenging position in the field of Data Science..."
        # summary['current_salary'] = "$90,000 per annum"
        return summary
    
    def parse_education(self, text):
        education = []
        education_pattern = re.compile(r'Education(.+?)(?:Experience|Skills|Certifications|Achievements)', re.DOTALL)
        matches = education_pattern.findall(text)
        if matches:
            for match in matches:
                education_info = {}
                # Extract school name
                school_match = re.search(r'([A-Za-z0-9 .,]+)', match)
                if school_match:
                    education_info["school"] = school_match.group(1).strip()
                # Extract degree name
                degree_match = re.search(r'(Bachelor|Master|Ph\.D\.|Doctorate) of ([A-Za-z0-9 .]+)', match)
                if degree_match:
                    education_info["degree_name"] = f"{degree_match.group(1)} of {degree_match.group(2)}"
                # Extract dates
                date_match = re.search(r'(\d{4}) - (\d{4}|\bPresent\b)', match)
                if date_match:
                    education_info["start_date"] = date_match.group(1)
                    education_info["end_date"] = date_match.group(2)
                # Extract description
                description_match = re.search(r'(?:GPA: ([\d.]+))|(?:(?<=\n)\w.+?)(?=\n)', match)
                if description_match:
                    education_info["description"] = description_match.group(0).strip()
                education.append(education_info)
        return education
    
    def parse_experience(self, text):
        experience = []
        experience_pattern = re.compile(r'Experience(.+?)(?:Education|Skills|Certifications|Achievements)', re.DOTALL)
        matches = experience_pattern.findall(text)
        if matches:
            for match in matches:
                experience_info = {}
                # Extract title
                title_match = re.search(r'([A-Za-z0-9 .,]+)', match)
                if title_match:
                    experience_info["title"] = title_match.group(1).strip()
                # Extract employer
                employer_match = re.search(r'(?:Employer:|Company:|Organization:)\s*([A-Za-z0-9 .,]+)', match)
                if employer_match:
                    experience_info["employer"] = employer_match.group(1).strip()
                # Extract dates
                date_match = re.search(r'(\d{4}) - (\d{4}|\bPresent\b)', match)
                if date_match:
                    experience_info["start_date"] = date_match.group(1)
                    experience_info["end_date"] = date_match.group(2)
                # Extract description
                description_match = re.search(r'(?:Responsibilities:|Description:)(.+?)(?:$|Education|Skills|Certifications|Achievements)', match, re.DOTALL)
                if description_match:
                    experience_info["description"] = description_match.group(1).strip()
                experience.append(experience_info)
        return experience
    
    # Add similar parsing methods for other fields
    # ...

    def parse_resume(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.pdf':
            text = self.parse_pdf(file_path)
        elif file_extension.lower() == '.docx':
            text = self.parse_word(file_path)
        else:
            raise ValueError("Unsupported file format. Only PDF and Word documents are supported.")
        
        resume_data = {}
        resume_data['personal'] = {
            "gender": "",
            "full_name": self.parse_name(text),
            "birthplace": "",
            "first_name": "",
            "family_name": "",
            "middle_name": "",
            "nationality": [],
            "picture_url": None,
            "date_of_birth": "",
            "marital_status": "",
            "picture_extension": None
        }
        resume_data['contact'] = {
            "email": [{"value": self.parse_email(text)}],
            "phone": [{"type": "Telephone", "value": self.parse_phone(text)}],
            "address": [],
            "website": []
        }
        
        # Call parsing functions for other fields
        resume_data['summary'] = self.parse_summary(text)
        resume_data['education'] = self.parse_education(text)
        resume_data['experience'] = self.parse_experience(text)
        
        # Add parsing logic for other fields
        # ...
        
        return resume_data

# Example usage:
resume_parser = EnglishResumeParser()
resume_data = resume_parser.parse_resume('Shashank_Sahoo_LLM_cv.pdf')

# Export resume data to a JSON file
with open('resume_data.json', 'w') as json_file:
    json.dump(resume_data, json_file, indent=4)

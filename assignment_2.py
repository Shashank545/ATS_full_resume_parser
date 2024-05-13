import re
import os
import json
from PyPDF2 import PdfReader
from docx import Document
from langdetect import detect

class MultilingualResumeParser:
    def __init__(self):
        pass
    
    def detect_language(self, text):
        """
        Detect the language of the resume text.
        
        Args:
        - text (str): Resume text.
        
        Returns:
        - language_code (str): ISO 639-1 language code of the detected language.
        """
        language_code = detect(text)
        return language_code
    
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
    
    def parse_name(self, text, language_code):
        """
        Extract the name from the resume text.
        
        Args:
        - text (str): Resume text.
        - language_code (str): ISO 639-1 language code of the resume text.
        
        Returns:
        - name (str): Extracted name.
        """
        name = None
        # Implement language-specific logic for extracting name
        # For example, for English resumes:
        if language_code == 'en':
            name_pattern = re.compile(r'([A-Z][a-z]+(?: [A-Z][a-z]+)?)')
            match = name_pattern.search(text)
            if match:
                name = match.group(0)
        # Add logic for other languages as needed
        return name
    
    def parse_email(self, text):
        """
        Extract the email address from the resume text.
        
        Args:
        - text (str): Resume text.
        
        Returns:
        - email (str): Extracted email address.
        """
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        match = email_pattern.search(text)
        if match:
            email = match.group(0)
        else:
            email = None
        return email
    
    def parse_phone(self, text):
        """
        Extract the phone number from the resume text.
        
        Args:
        - text (str): Resume text.
        
        Returns:
        - phone (str): Extracted phone number.
        """
        phone_pattern = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        match = phone_pattern.search(text)
        if match:
            phone = match.group(0)
        else:
            phone = None
        return phone
    
    def parse_summary(self, text, language_code):
        """
        Extract the summary section from the resume text.
        
        Args:
        - text (str): Resume text.
        - language_code (str): ISO 639-1 language code of the resume text.
        
        Returns:
        - summary_data (dict): Parsed summary data.
        """
        # Implement language-specific logic for parsing summary
        # For example, for English resumes:
        if language_code == 'en':
            # Assuming summary section starts with "Summary" or "Objective" heading
            summary_pattern = re.compile(r'(Summary|Objective):(.+)', re.IGNORECASE)
            match = summary_pattern.search(text)
            if match:
                summary_text = match.group(2).strip()
            else:
                summary_text = ""
        # Add logic for other languages as needed
        return {
            "benefits": "",
            "objective": "",
            "description": summary_text,
            "notice_period": "",
            "current_salary": ""
        }
    
    def parse_education(self, text, language_code):
        """
        Extract the education section from the resume text.
        
        Args:
        - text (str): Resume text.
        - language_code (str): ISO 639-1 language code of the resume text.
        
        Returns:
        - education_data (list): Parsed education data.
        """
        # Implement language-specific logic for parsing education
        # For example, for English resumes:
        if language_code == 'en':
            # Assuming education section starts with "Education" heading
            education_pattern = re.compile(r'Education:(.+?)Experience:', re.IGNORECASE | re.DOTALL)
            match = education_pattern.search(text)
            if match:
                education_text = match.group(1).strip()
                # Assuming each education entry starts with the institution/school name
                education_entries = education_text.split('\n\n')
                education_data = []
                for entry in education_entries:
                    entry_lines = entry.split('\n')
                    school_name = entry_lines[0].strip()
                    description = '\n'.join(entry_lines[1:]).strip()
                    education_data.append({
                        "city": "",
                        "school": school_name,
                        "country": "",
                        "end_date": "",
                        "start_date": "",
                        "degree_name": "",
                        "description": description,
                        "country_code": "",
                        "degree_major": "",
                        "custom_sections": []
                    })
            else:
                education_data = []
        # Add logic for other languages as needed
        return education_data
    
    def parse_experience(self, text, language_code):
        """
        Extract the experience section from the resume text.
        
        Args:
        - text (str): Resume text.
        - language_code (str): ISO 639-1 language code of the resume text.
        
        Returns:
        - experience_data (list): Parsed experience data.
        """
        # Implement language-specific logic for parsing experience
        # For example, for English resumes:
        if language_code == 'en':
            # Assuming experience section starts with "Experience" heading
            experience_pattern = re.compile(r'Experience:(.+?)Education:', re.IGNORECASE | re.DOTALL)
            match = experience_pattern.search(text)
            if match:
                experience_text = match.group(1).strip()
                # Assuming each experience entry starts with the job title
                experience_entries = experience_text.split('\n\n')
                experience_data = []
                for entry in experience_entries:
                    entry_lines = entry.split('\n')
                    title = entry_lines[0].strip()
                    employer = entry_lines[1].strip()
                    description = '\n'.join(entry_lines[2:]).strip()
                    experience_data.append({
                        "city": "",
                        "title": title,
                        "country": "",
                        "employer": employer,
                        "end_date": "",
                        "start_date": "",
                        "description": description,
                        "country_code": "",
                        "custom_sections": []
                    })
            else:
                experience_data = []
        # Add logic for other languages as needed
        return experience_data
    
    def parse_resume(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.pdf':
            text = self.parse_pdf(file_path)
        elif file_extension.lower() == '.docx':
            text = self.parse_word(file_path)
        else:
            raise ValueError("Unsupported file format. Only PDF and Word documents are supported.")
        
        # Detect the language of the resume
        language_code = self.detect_language(text)
        
        resume_data = {}
        resume_data['personal'] = {
            "gender": "",
            "full_name": self.parse_name(text, language_code),
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
        
        # Call language-specific parsing functions for other fields
        resume_data['summary'] = self.parse_summary(text, language_code)
        resume_data['education'] = self.parse_education(text, language_code)
        resume_data['experience'] = self.parse_experience(text, language_code)
        
        # Add parsing logic for other fields
        # ...
        
        return resume_data

# Example usage:
resume_parser = MultilingualResumeParser()
resume_data = resume_parser.parse_resume('Shashank_Resume_Data_Science_Expert.pdf')

# Export resume data to a JSON file
with open('resume_data.json', 'w') as json_file:
    json.dump(resume_data, json_file, indent=4)

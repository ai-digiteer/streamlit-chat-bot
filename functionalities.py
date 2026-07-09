from PIL import Image
import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import google.generativeai as genai

from io import BytesIO
import base64
import docx
import csv
import PyPDF2

from dotenv import load_dotenv
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_image_with_ai(image_file):
    """Analyze image using Gemini 2.5 Flash - supports any type of image including handwritten text and receipts"""
    try:
        image_file.seek(0)
        image_data = image_file.read()
        
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = """You are an advanced OCR and image analysis system. Analyze this image thoroughly and extract ALL information:

        PRIMARY TASKS:
        1. **Text Extraction (OCR)**: Extract ALL visible text, including:
           - Printed text
           - HANDWRITTEN text (cursive, print, notes)
           - Text in any language
           - Numbers, dates, codes
        
        2. **Document Analysis**: If this is a document, identify:
           - Document type (receipt, invoice, form, letter, note, etc.)
           - Key information (dates, amounts, names, addresses, phone numbers)
           - Line items, totals, calculations
           - Signatures or stamps
        
        3. **Receipt/Invoice Analysis**: If this is a receipt or invoice, extract:
           - Store/business name and location
           - Date and time of transaction
           - Itemized list with prices
           - Subtotals, taxes, discounts
           - Total amount
           - Payment method
           - Receipt/transaction number
        
        4. **Visual Content**: Describe what you see:
           - Objects, products, people, scenes
           - Brands, logos, labels
           - Colors, layout, condition
           - Any relevant visual details
        
        5. **Handwritten Notes**: Pay special attention to handwritten content:
           - Transcribe handwritten text as accurately as possible
           - Note if handwriting is unclear
           - Capture margin notes, annotations, signatures
        
        Provide a comprehensive, structured analysis with all extracted information."""
        
        response = model.generate_content([
            {"mime_type": image_file.type, "data": image_data},
            prompt
        ])
        return response.text
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}"
        
def analyze_pdf_with_ai(pdf_file):
    """Analyze PDF using Gemini 2.5 Flash natively - handles text, layout, handwriting, and tables"""
    try:
        pdf_file.seek(0)
        pdf_bytes = pdf_file.read()
        
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = """Analyze this PDF document thoroughly. Extract and summarize ALL information including:
        - Printed text and structure
        - Tables, charts, and structured data
        - Handwritten text, notes, or annotations
        - Key metadata, signatures, stamps, or marks
        
        Provide a comprehensive analysis of the document content."""
        
        response = model.generate_content([
            {"mime_type": "application/pdf", "data": pdf_bytes},
            prompt
        ])
        return response.text
            
    except Exception as e:
        return f"Error analyzing PDF: {str(e)}"
    
def read_uploaded_file(file):
    file_type = file.type
    
    if file_type == "text/plain":
        return file.read().decode("utf-8")

    elif file_type == "application/pdf":
        return analyze_pdf_with_ai(file)

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_type == "text/csv":
        csv_text = ""
        decoded = file.read().decode("utf-8").splitlines()
        reader = csv.reader(decoded)
        for row in reader:
            csv_text += ", ".join(row) + "\n"
        return csv_text

    else:
        return "❌ Unsupported file type"

    
    
def load_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "prompt.md")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "You are Digiteer AI, a helpful virtual assistant."

def ask_ai(question, documents=""):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt_base = load_prompt()
    prompt_template_text = f"""{prompt_base}

---

User Question: {{question}}
Documents/Context: {{documents}}
"""

    prompt_template = ChatPromptTemplate.from_template(prompt_template_text)
    ai_chain = prompt_template | llm | StrOutputParser()

    try:
        return ai_chain.invoke({"question": question, "documents": documents})
    except Exception as e:
        return f"Error: {e}"

    
    
    
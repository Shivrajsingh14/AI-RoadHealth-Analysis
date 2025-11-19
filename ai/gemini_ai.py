import google.generativeai as genai
import json
import logging
from django.conf import settings
from PIL import Image
import os

# Configure logging
logger = logging.getLogger(__name__)

class GeminiAI:
    def __init__(self):
        """Initialize Gemini AI with API key from settings"""
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in settings. Please set it in your .env file.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
    
    def analyze_road_image(self, image_path):
        """
        Analyze road/pavement image using Gemini Vision API
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Analysis results or None if failed
        """
        try:
            # Validate image exists
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return None
            
            # Open and validate image
            try:
                img = Image.open(image_path)
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
            except Exception as e:
                logger.error(f"Error opening image: {e}")
                return None
            
            # Prepare the prompt
            prompt = """
            Analyze the given road or pavement image. Identify:
            - Crack percentage  
            - Pothole probability (0–1)  
            - Surface damage  
            - Severity (Low, Medium, High)  
            - Condition score (0–100)

            Return STRICT JSON only like:
            {
              "crack_percentage": 23.5,
              "pothole_probability": 0.8,
              "severity": "High",
              "condition_score": 45
            }
            
            Important: Return ONLY the JSON object, no additional text or explanations.
            """
            
            # Generate content with image
            response = self.model.generate_content([prompt, img])
            
            if not response or not response.text:
                logger.error("Empty response from Gemini API")
                return None
            
            # Parse JSON response
            try:
                # Clean the response text
                response_text = response.text.strip()
                
                # Remove markdown formatting if present
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                
                response_text = response_text.strip()
                
                # Parse JSON
                result = json.loads(response_text)
                
                # Validate required fields
                required_fields = ['crack_percentage', 'pothole_probability', 'severity', 'condition_score']
                for field in required_fields:
                    if field not in result:
                        logger.error(f"Missing required field: {field}")
                        return None
                
                # Validate data types and ranges
                if not isinstance(result['crack_percentage'], (int, float)) or result['crack_percentage'] < 0 or result['crack_percentage'] > 100:
                    logger.error("Invalid crack_percentage value")
                    return None
                
                if not isinstance(result['pothole_probability'], (int, float)) or result['pothole_probability'] < 0 or result['pothole_probability'] > 1:
                    logger.error("Invalid pothole_probability value")
                    return None
                
                if result['severity'] not in ['Low', 'Medium', 'High']:
                    logger.error("Invalid severity value")
                    return None
                
                if not isinstance(result['condition_score'], int) or result['condition_score'] < 0 or result['condition_score'] > 100:
                    logger.error("Invalid condition_score value")
                    return None
                
                logger.info(f"Successfully analyzed image: {image_path}")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Raw response: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error analyzing image with Gemini AI: {e}")
            return None
    
    def test_connection(self):
        """Test if Gemini AI connection is working"""
        try:
            # Simple test with text generation
            response = self.model.generate_content("Hello, respond with 'Connection successful!'")
            return response and response.text and "successful" in response.text.lower()
        except Exception as e:
            logger.error(f"Gemini AI connection test failed: {e}")
            return False


def analyze_road_condition(image_path):
    """
    Convenience function to analyze road condition
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        dict: Analysis results or None if failed
    """
    try:
        gemini = GeminiAI()
        return gemini.analyze_road_image(image_path)
    except Exception as e:
        logger.error(f"Error in analyze_road_condition: {e}")
        return None
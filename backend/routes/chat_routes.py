"""
AI Chatbot routes for Smart PG Recommendation App
Integrates with Groq API for intelligent responses
"""

from flask import Blueprint, request, jsonify
import json
import os
import re
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create blueprint
bp = Blueprint('chat', __name__, url_prefix='/api/chat')

def get_db_and_recommender():
    """Get db and recommender instances"""
    from app import db
    from ml_model import get_recommendations
    return db, get_recommendations

def token_required(f):
    """Optional token requirement for chat (can be used without login too)"""
    @wraps(f)
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated

def call_groq_api(user_message, context=""):
    """
    Call Groq API for intelligent response
    
    Args:
        user_message: User's message
        context: Additional context about available PGs
        
    Returns:
        str: AI response or None if API fails
    """
    try:
        import requests
        
        groq_api_key = os.getenv('GROQ_API_KEY')
        groq_model = os.getenv('GROQ_MODEL', 'mixtral-8x7b-32768')
        
        if not groq_api_key or groq_api_key == 'your_groq_api_key_here':
            return None  # API key not configured
        
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = """You are a helpful PG (Paying Guest) recommendation assistant. 
You help users find suitable accommodation. Keep responses concise and helpful.
Provide specific recommendations when possible.
If the user asks about PGs, help them filter by city, budget, type, furnishing, or tenant type."""
        
        full_context = f"User context: {context}" if context else ""
        
        payload = {
            "model": groq_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_message}\n{full_context}"}
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"Groq API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Groq API call failed: {str(e)}")
        return None

class ChatbotEngine:
    """AI Chatbot Engine with Intent Recognition and Groq Integration"""
    
    def __init__(self):
        self.intents = {
            'find_budget': ['budget', 'price', 'under', 'cost', 'afford', 'less than'],
            'find_location': ['city', 'area', 'locality', 'where', 'location', 'place'],
            'find_type': ['bhk', 'bedroom', 'room', '1bhk', '2bhk', '3bhk', 'rooms'],
            'find_furnish': ['furnished', 'unfurnished', 'semi-furnished', 'furnish'],
            'find_tenant': ['bachelor', 'bachelors', 'family', 'tenant', 'girls', 'boys'],
            'show_all': ['show', 'list', 'all', 'any', 'all pgs', 'available'],
            'help': ['help', 'what can you do', 'features', 'how does this work']
        }
    
    def extract_intent(self, message):
        """Extract user intent from message"""
        message_lower = message.lower()
        detected_intents = []
        
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in message_lower:
                    detected_intents.append(intent)
                    break
        
        return detected_intents if detected_intents else ['show_all']
    
    def extract_entities(self, message):
        """Extract entities like budget, city, bhk from message"""
        from difflib import get_close_matches
        entities = {}
        message_lower = message.lower()
        
        # Extract budget (numbers)
        budget_match = re.search(r'(\d+)\s*(k|thousand)?', message_lower)
        if budget_match:
            amount = int(budget_match.group(1))
            if budget_match.group(2):  # If 'k' or 'thousand'
                amount *= 1000
            entities['max_budget'] = amount
        
        # Extract city - look for common Indian cities with fuzzy matching
        cities = ['bangalore', 'mumbai', 'delhi', 'pune', 'chennai', 'kolkata', 
                 'hyderabad', 'noida', 'gurgaon', 'ahmedabad', 'jaipur']
        
        # Extract potential city words from message
        words = message_lower.split()
        for word in words:
            # Try exact match first
            if word in cities:
                entities['city'] = word.capitalize()
                break
            # Try fuzzy matching for typos
            matches = get_close_matches(word, cities, n=1, cutoff=0.6)
            if matches:
                entities['city'] = matches[0].capitalize()
                break
        
        # Extract BHK
        bhk_match = re.search(r'(\d)\s*bhk', message_lower)
        if bhk_match:
            entities['bhk'] = int(bhk_match.group(1))
        
        # Extract tenant type
        if 'bachelor' in message_lower or 'boys' in message_lower:
            entities['tenant_type'] = 'Bachelors'
        elif 'family' in message_lower:
            entities['tenant_type'] = 'Family'
        elif 'girls' in message_lower:
            entities['tenant_type'] = 'Bachelors (Female)'
        
        return entities
    
    def generate_response(self, message, intents, entities, recommendations=None):
        """Generate AI response using Groq API or fallback"""
        
        if 'help' in intents:
            return {
                'type': 'help',
                'message': '''🤖 I'm your Smart PG Assistant! Here's what I can help you with:

1. **Find PGs by Budget**: "Show me PGs under 10k" or "Find affordable PGs"
2. **Find PGs by Location**: "Show me PGs in Bangalore" or "What's available in Pune?"
3. **Find by Type**: "Show me 2BHK" or "Find 3 bedroom places"
4. **Find by Tenant**: "Bachelors friendly" or "Family accommodations"
5. **Find Furnished**: "Furnished PGs" or "Semi-furnished options"

You can also combine filters: "Show me 2BHK furnished PGs under 15k in Bangalore"

How can I help you today?'''
            }
        
        # If we have recommendations, return them
        if recommendations and len(recommendations) > 0:
            msg = f"✅ Found {len(recommendations)} matching PGs! Here are the best options:"
            return {
                'type': 'recommendations',
                'message': msg,
                'recommendations': recommendations[:5],
                'filters_applied': entities
            }
        
        # If filters were provided but no results
        if entities and any(v for v in entities.values()):
            msg = f"❌ Sorry, I couldn't find any PGs matching your criteria: {self._format_filters(entities)}. Try adjusting your filters or try a different location."
            return {
                'type': 'no_results',
                'message': msg,
                'filters_applied': entities,
                'suggestions': [
                    'Try a higher budget',
                    'Try a different city',
                    'Try "Show all PGs"'
                ]
            }
        
        # Try to use Groq API for general question
        groq_response = call_groq_api(message)
        
        if groq_response:
            return {
                'type': 'info',
                'message': groq_response
            }
        else:
            return {
                'type': 'info',
                'message': f"I understood you're looking for {self._format_filters(entities)}. Let me search for options...",
                'filters': entities
            }
    
    def _format_filters(self, entities):
        """Format entities into readable text"""
        parts = []
        if entities.get('city'):
            parts.append(f"PGs in {entities['city']}")
        if entities.get('max_budget'):
            parts.append(f"under ₹{entities['max_budget']}")
        if entities.get('bhk'):
            parts.append(f"{entities['bhk']}BHK")
        if entities.get('tenant_type'):
            parts.append(f"{entities['tenant_type']}")
        
        return " ".join(parts) if parts else "PGs"


# Initialize chatbot engine
chatbot = ChatbotEngine()

@bp.route('/message', methods=['POST'])
@token_required
def chat_message():
    """
    Process user message and return chatbot response
    
    Request body:
    {
        "message": "string"
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('message'):
            return jsonify({
                'status': 'error',
                'message': 'Message is required'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'status': 'error',
                'message': 'Message cannot be empty'
            }), 400
        
        # Extract intent and entities
        intents = chatbot.extract_intent(user_message)
        entities = chatbot.extract_entities(user_message)
        
        # Get recommendations if applicable
        recommendations = None
        db, get_recommendations_fn = get_db_and_recommender()
        
        if not ('help' in intents):
            recommendations = get_recommendations_fn(
                entities.get('city'),
                entities.get('max_budget'),
                entities.get('tenant_type'),
                entities.get('bhk'),
                5
            )
        
        # Generate response
        response = chatbot.generate_response(user_message, intents, entities, recommendations)
        
        return jsonify({
            'status': 'success',
            'response': response,
            'intents': intents,
            'entities': entities
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Chat error: {str(e)}'
        }), 500

@bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get chatbot suggestions for the user"""
    try:
        suggestions = [
            "Find PGs under 10k",
            "Show me 2BHK in Bangalore",
            "Bachelors friendly PGs",
            "Furnished PGs",
            "Show all available options"
        ]
        
        return jsonify({
            'status': 'success',
            'suggestions': suggestions
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error fetching suggestions: {str(e)}'
        }), 500

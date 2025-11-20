import json
import random
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ConversationEngine:
    def __init__(self, portraits_path=None, use_llm=True):
        if portraits_path is None:
            portraits_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "portraits.json")
        
        if os.path.exists(portraits_path):
            with open(portraits_path, 'r') as f:
                self.portraits = json.load(f)
        else:
            # Fallback default portraits
            self.portraits = {
                "fat_lady": {
                    "name": "The Fat Lady",
                    "personality": "Sassy, dramatic, loves compliments and gossip",
                    "voice": {"pitch": 1.3, "speed": 0.9, "style": "theatrical"},
                    "typical_phrases": ["Oh my STARS!", "How absolutely DRAMATIC!", "I simply CANNOT believe it!"]
                },
                "sir_cadogan": {
                    "name": "Sir Cadogan",
                    "personality": "Bold, brave, slightly mad knight who challenges everything",
                    "voice": {"pitch": 0.7, "speed": 1.2, "style": "booming"},
                    "typical_phrases": ["EN GARDE!", "I challenge thee to a DUEL!", "Forward to GLORY!"]
                }
            }
        
        self.use_llm = use_llm
        self.client = None
        
        # Initialize OpenAI client if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if use_llm and api_key:
            try:
                self.client = OpenAI(api_key=api_key)
                print("✅ OpenAI client initialized")
            except Exception as e:
                print(f"⚠️ Could not initialize OpenAI: {e}")
                print("⚠️ Falling back to template mode")
                self.use_llm = False
        else:
            if use_llm:
                print("⚠️ OPENAI_API_KEY not found in environment")
                print("⚠️ Using template mode. Set OPENAI_API_KEY to enable LLM conversations")
            self.use_llm = False
    
    def generate_dialogue(self, trigger_object, visitor_name):
        """
        Creates 4-turn conversation about detected object using LLM
        """
        
        # Select 2-3 portraits to participate
        available_portraits = list(self.portraits.keys())
        num_participants = min(3, len(available_portraits))
        participants = random.sample(available_portraits, num_participants)
        
        conversation = []
        previous_lines = []  # Track conversation for context
        
        # Turn 1: First portrait reacts
        portrait1 = participants[0]
        portrait1_name = self.portraits[portrait1].get("name", portrait1)
        line1 = self._generate_line(
            portrait=portrait1,
            object=trigger_object,
            context="initial_reaction",
            visitor_name=visitor_name,
            previous_lines=previous_lines
        )
        conversation.append({
            "portrait": portrait1,
            "text": line1,
            "voice": self.portraits[portrait1].get("voice", {})
        })
        previous_lines.append({"speaker": portrait1_name, "text": line1})
        
        # Turn 2: Second portrait responds
        if len(participants) > 1:
            portrait2 = participants[1]
            portrait2_name = self.portraits[portrait2].get("name", portrait2)
            line2 = self._generate_line(
                portrait=portrait2,
                object=trigger_object,
                context=f"respond_to: {line1}",
                visitor_name=visitor_name,
                previous_lines=previous_lines
            )
            conversation.append({
                "portrait": portrait2,
                "text": line2,
                "voice": self.portraits[portrait2].get("voice", {})
            })
            previous_lines.append({"speaker": portrait2_name, "text": line2})
        
        # Turn 3: Third portrait or first portrait continues
        if len(participants) > 2:
            portrait3 = participants[2]
            portrait3_name = self.portraits[portrait3].get("name", portrait3)
            line3 = self._generate_line(
                portrait=portrait3,
                object=trigger_object,
                context=f"continue_conversation: {line1} {line2}",
                visitor_name=visitor_name,
                previous_lines=previous_lines
            )
            conversation.append({
                "portrait": portrait3,
                "text": line3,
                "voice": self.portraits[portrait3].get("voice", {})
            })
            previous_lines.append({"speaker": portrait3_name, "text": line3})
        
        # Turn 4: Wrap up
        final_portrait = participants[0]
        final_portrait_name = self.portraits[final_portrait].get("name", final_portrait)
        line4 = self._generate_line(
            portrait=final_portrait,
            object=trigger_object,
            context="conclusion",
            visitor_name=visitor_name,
            previous_lines=previous_lines
        )
        conversation.append({
            "portrait": final_portrait,
            "text": line4,
            "voice": self.portraits[final_portrait].get("voice", {})
        })
        previous_lines.append({"speaker": final_portrait_name, "text": line4})
        
        return conversation
    
    def _generate_line(self, portrait, object, context, visitor_name="stranger", previous_lines=None):
        """
        Use AI model to generate portrait's line
        """
        personality = self.portraits[portrait].get("personality", "")
        portrait_name = self.portraits[portrait].get("name", portrait)
        typical_phrases = self.portraits[portrait].get("typical_phrases", [])
        
        # Try to use LLM if available
        if self.use_llm and self.client:
            try:
                return self._generate_llm_line(
                    portrait_name=portrait_name,
                    personality=personality,
                    object=object,
                    context=context,
                    visitor_name=visitor_name,
                    previous_lines=previous_lines or []
                )
            except Exception as e:
                print(f"⚠️ LLM generation failed: {e}")
                print("⚠️ Falling back to templates")
        
        # Fallback to templates
        templates = {
            "fat_lady": [
                f"Oh my! Is that a {object}? How DRAMATIC!",
                f"Goodness gracious, {visitor_name}! A {object}? I simply CANNOT believe it!",
                f"Stars above! A {object}? How absolutely fascinating!"
            ],
            "sir_cadogan": [
                f"A {object}?! I challenge it to a DUEL!",
                f"EN GARDE, {object}! Face me in combat!",
                f"Forward to GLORY! That {object} shall not pass!"
            ],
            "headmaster": [
                f"Hmm, a {object}... most intriguing, {visitor_name}.",
                f"The {object} speaks of mysteries yet untold.",
                f"Interesting, {visitor_name}. The {object} reveals much."
            ],
            "mermaid": [
                f"Bubbles and waves! A {object} floats into view!",
                f"Oh {visitor_name}, the {object} dances like a current!",
                f"Splash! A {object} appears, like treasure from the deep!"
            ],
            "ambrose": [
                f"Well, well, {visitor_name}. A {object}. How... ordinary.",
                f"I suppose a {object} is acceptable, though hardly remarkable.",
                f"Hmph. A {object}. One must maintain standards, after all."
            ]
        }
        
        if portrait in templates:
            return random.choice(templates[portrait])
        elif typical_phrases:
            return f"{random.choice(typical_phrases)} I see a {object}!"
        else:
            return f"Interesting {object}!"
    
    def _generate_llm_line(self, portrait_name, personality, object, context, visitor_name, previous_lines):
        """
        Generate a line using OpenAI's LLM
        """
        # Build context from previous conversation
        conversation_context = ""
        if previous_lines:
            conversation_context = "\n\nPrevious conversation:\n"
            for line in previous_lines:
                conversation_context += f"{line['speaker']}: {line['text']}\n"
        
        # Create prompt based on context
        if context == "initial_reaction":
            user_prompt = f"A visitor named {visitor_name} has just shown you a {object}. React to it in character. Keep it to 1-2 short sentences."
        elif "respond_to:" in context:
            user_prompt = f"Respond to what was just said about the {object} that {visitor_name} showed. Stay in character. Keep it to 1-2 short sentences.{conversation_context}"
        elif "continue_conversation:" in context:
            user_prompt = f"Continue the conversation about the {object}. Add your unique perspective. Keep it to 1-2 short sentences.{conversation_context}"
        elif context == "conclusion":
            user_prompt = f"Make a final comment about the {object} to wrap up the conversation. Keep it to 1-2 short sentences.{conversation_context}"
        else:
            user_prompt = f"Comment on the {object} that {visitor_name} showed. Keep it to 1-2 short sentences."
        
        system_prompt = f"""You are {portrait_name}, a magical talking portrait.

Your personality: {personality}

Important rules:
- Stay completely in character
- Keep responses to 1-2 SHORT sentences (under 100 characters total if possible)
- Be expressive and use your personality traits
- React naturally to the object and other portraits
- Don't break the fourth wall
- Don't explain yourself, just be you"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Fast and cost-effective
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=60,
                temperature=0.8,  # More creative
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            # Remove quotes if LLM added them
            if generated_text.startswith('"') and generated_text.endswith('"'):
                generated_text = generated_text[1:-1]
            
            print(f"✅ Generated for {portrait_name}: {generated_text}")
            return generated_text
            
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            raise


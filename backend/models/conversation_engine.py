import json
import random
import os

class ConversationEngine:
    def __init__(self, portraits_path=None):
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
    
    def generate_dialogue(self, trigger_object, visitor_name):
        """
        Creates 4-turn conversation about detected object
        Option 1: Use local Phi-3 model
        Option 2: Use OpenAI/Claude API (easier)
        """
        
        # Select 2-3 portraits to participate
        available_portraits = list(self.portraits.keys())
        num_participants = min(3, len(available_portraits))
        participants = random.sample(available_portraits, num_participants)
        
        conversation = []
        
        # Turn 1: First portrait reacts
        portrait1 = participants[0]
        line1 = self._generate_line(
            portrait=portrait1,
            object=trigger_object,
            context="initial_reaction",
            visitor_name=visitor_name
        )
        conversation.append({
            "portrait": portrait1,
            "text": line1,
            "voice": self.portraits[portrait1].get("voice", {})
        })
        
        # Turn 2: Second portrait responds
        if len(participants) > 1:
            portrait2 = participants[1]
            line2 = self._generate_line(
                portrait=portrait2,
                object=trigger_object,
                context=f"respond_to: {line1}",
                visitor_name=visitor_name
            )
            conversation.append({
                "portrait": portrait2,
                "text": line2,
                "voice": self.portraits[portrait2].get("voice", {})
            })
        
        # Turn 3: Third portrait or first portrait continues
        if len(participants) > 2:
            portrait3 = participants[2]
            line3 = self._generate_line(
                portrait=portrait3,
                object=trigger_object,
                context=f"continue_conversation: {line1} {line2}",
                visitor_name=visitor_name
            )
            conversation.append({
                "portrait": portrait3,
                "text": line3,
                "voice": self.portraits[portrait3].get("voice", {})
            })
        
        # Turn 4: Wrap up
        final_portrait = participants[0]
        line4 = self._generate_line(
            portrait=final_portrait,
            object=trigger_object,
            context="conclusion",
            visitor_name=visitor_name
        )
        conversation.append({
            "portrait": final_portrait,
            "text": line4,
            "voice": self.portraits[final_portrait].get("voice", {})
        })
        
        return conversation
    
    def _generate_line(self, portrait, object, context, visitor_name="stranger"):
        """
        Use AI model to generate portrait's line
        """
        personality = self.portraits[portrait].get("personality", "")
        typical_phrases = self.portraits[portrait].get("typical_phrases", [])
        
        # OPTION A: Simple template (no AI needed)
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
        
        # OPTION B: Use OpenAI API (uncomment to use)
        # import openai
        # response = openai.chat.completions.create(
        #     model="gpt-4",
        #     messages=[{
        #         "role": "system",
        #         "content": f"You are {portrait}. Personality: {personality}"
        #     }, {
        #         "role": "user",
        #         "content": f"React to seeing a {object}. {context}"
        #     }]
        # )
        # return response.choices[0].message.content


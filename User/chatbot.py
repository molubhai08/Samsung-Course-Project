from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

class TherapistChatbot:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.system_prompt = """You are a compassionate and empathetic therapist AI assistant. Your role is to:

- Listen actively and provide supportive responses
- Ask thoughtful follow-up questions to help users explore their feelings
- Offer gentle guidance and coping strategies when appropriate
- Validate emotions without judgment
- Maintain a warm, professional, and caring tone
- Never diagnose mental health conditions
- Encourage professional help when needed

You will receive messages that include the user's detected emotion in brackets. Use this emotional context to provide more empathetic and relevant responses, but respond naturally without explicitly mentioning the emotion detection.

Keep responses conversational, supportive, and concise (2-4 sentences typically)."""

    def get_response(self, user_message, emotion, conversation_history=None):
        """
        Get chatbot response with emotion context.
        
        Args:
            user_message: The user's text input
            emotion: Detected emotion (e.g., 'Sadness', 'Joy')
            conversation_history: List of previous messages [(role, text), ...]
        
        Returns:
            Bot response text
        """
        messages = [SystemMessage(content=self.system_prompt)]
        
        # Add conversation history
        if conversation_history:
            for role, text in conversation_history[-10:]:  # Last 10 messages for context
                if role == 'USER':
                    messages.append(HumanMessage(content=text))
                else:
                    messages.append(AIMessage(content=text))
        
        # Add current message with emotion context
        enhanced_message = f"[Detected emotion: {emotion}] {user_message}"
        messages.append(HumanMessage(content=enhanced_message))
        
        response = self.llm.invoke(messages)
        return response.content

# Global instance
_chatbot = None

def get_chatbot():
    global _chatbot
    if _chatbot is None:
        _chatbot = TherapistChatbot()
    return _chatbot

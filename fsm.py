# fsm.py - Finite State Machine untuk INA-BOT Chatbot

from enum import Enum
from typing import Dict, Any, Optional

class ChatState(Enum):
    IDLE = "idle"
    ASKING_CITY = "asking_city"
    SHOWING_RISK = "showing_risk"
    EMERGENCY_MODE = "emergency_mode"
    GUIDE_MODE = "guide_mode"


class ChatFSM:
    def __init__(self):
        self.current_state = ChatState.IDLE
        self.context = {}
        self.state_history = []
        
        self.transitions = {
            ChatState.IDLE: {
                'ask_city': ChatState.ASKING_CITY,
                'emergency': ChatState.EMERGENCY_MODE,
                'guide': ChatState.GUIDE_MODE,
                'city_detected': ChatState.SHOWING_RISK
            },
            ChatState.ASKING_CITY: {
                'city_provided': ChatState.SHOWING_RISK,
                'cancel': ChatState.IDLE,
            },
            ChatState.SHOWING_RISK: {
                'emergency': ChatState.EMERGENCY_MODE,
                'back': ChatState.IDLE,
                'new_city': ChatState.ASKING_CITY,
            },
            ChatState.EMERGENCY_MODE: {
                'confirmed': ChatState.IDLE,
                'cancel': ChatState.IDLE,
            },
            ChatState.GUIDE_MODE: {
                'back': ChatState.IDLE,
                'city_detected': ChatState.SHOWING_RISK,
            }
        }
    
    def transition(self, event: str, input_data: Optional[Dict] = None) -> ChatState:
        if self.current_state in self.transitions:
            if event in self.transitions[self.current_state]:
                new_state = self.transitions[self.current_state][event]
                self.state_history.append({
                    'from': self.current_state.value,
                    'to': new_state.value,
                    'event': event
                })
                self.current_state = new_state
                
                if input_data:
                    self.context.update(input_data)
                
                return new_state
        return self.current_state
    
    def set_context(self, key: str, value: Any):
        self.context[key] = value
    
    def get_context(self, key: str, default=None):
        return self.context.get(key, default)
    
    def reset(self):
        self.current_state = ChatState.IDLE
        self.context = {}
    
    def is_emergency_mode(self):
        return self.current_state == ChatState.EMERGENCY_MODE


class ConversationManager:
    def __init__(self):
        self.fsm = ChatFSM()
        
        self.prompts = {
            ChatState.ASKING_CITY: "📍 Silakan sebutkan nama kota Anda. Contoh: 'Bandung', 'Jakarta'",
            ChatState.EMERGENCY_MODE: "🚨 **MODE DARURAT** - Apakah Anda membutuhkan bantuan? (YA/TIDAK)",
            ChatState.GUIDE_MODE: "📖 **PANDUAN:** 1.Tas Siaga 2.Jalur Evakuasi 3.Nomor Darurat 4.Kembali",
        }
    
    def process_message(self, message: str, intent: str, detected_city: Optional[Dict] = None) -> Dict:
        message_lower = message.lower()
        
        if self.fsm.current_state == ChatState.ASKING_CITY:
            if detected_city:
                self.fsm.set_context('last_city', detected_city)
                self.fsm.transition('city_provided')
                return {'response': None, 'state': self.fsm.get_state_info(), 'city_detected': detected_city}
            elif 'batal' in message_lower:
                self.fsm.transition('cancel')
                return {'response': "Kembali ke menu utama.", 'state': self.fsm.get_state_info(), 'city_detected': None}
        
        elif self.fsm.current_state == ChatState.EMERGENCY_MODE:
            if 'ya' in message_lower:
                self.fsm.transition('confirmed')
                return {'response': "🚨 Tim akan segera menghubungi Anda! Tetap tenang dan cari tempat aman.", 'state': self.fsm.get_state_info(), 'city_detected': None}
            elif 'tidak' in message_lower:
                self.fsm.transition('cancel')
                return {'response': "Mode darurat dinonaktifkan.", 'state': self.fsm.get_state_info(), 'city_detected': None}
        
        return {'response': None, 'state': self.fsm.get_state_info(), 'city_detected': detected_city}
    
    def get_prompt(self):
        if self.fsm.current_state in self.prompts:
            return self.prompts[self.fsm.current_state]
        return None
    
    def reset(self):
        self.fsm.reset()


def get_conversation_manager():
    return ConversationManager()
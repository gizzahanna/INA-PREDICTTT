# engine.py - AI Prediction Engine untuk INA-PREDICT

import random
from datetime import datetime, timedelta

class DisasterPredictionEngine:
    def __init__(self):
        self.prediction_accuracy = 94.7
        
        # Data histori bencana per provinsi
        self.historical_data = {
            'Jawa Barat': {'banjir': 456, 'gempa': 189, 'longsor': 234},
            'Jawa Timur': {'banjir': 378, 'gempa': 123, 'longsor': 167},
            'Jawa Tengah': {'banjir': 345, 'gempa': 134, 'longsor': 189},
            'Banten': {'banjir': 189, 'gempa': 78, 'longsor': 67},
            'Sumatera Barat': {'banjir': 167, 'gempa': 234, 'longsor': 78},
            'Papua': {'banjir': 89, 'gempa': 145, 'longsor': 78},
            'DKI Jakarta': {'banjir': 234, 'gempa': 23, 'longsor': 12},
        }
        
        # Parameter real-time (simulasi)
        self.real_time_params = {
            'rainfall': random.uniform(20, 180),
            'seismic_activity': random.randint(10, 150),
            'wind_speed': random.uniform(10, 70),
        }
    
    def calculate_risk_score(self, province):
        if province not in self.historical_data:
            return 50
        
        hist = self.historical_data[province]
        total_events = sum(hist.values())
        historical_risk = min(100, (total_events / 500) * 100)
        
        rainfall_risk = min(100, (self.real_time_params['rainfall'] / 200) * 100)
        seismic_risk = min(100, (self.real_time_params['seismic_activity'] / 200) * 100)
        
        risk = (historical_risk * 0.5) + (rainfall_risk * 0.3) + (seismic_risk * 0.2)
        return round(min(100, max(0, risk)), 1)
    
    def predict_weekly(self, province):
        base_risk = self.calculate_risk_score(province)
        predictions = []
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        
        for i, day in enumerate(days):
            variation = random.uniform(-0.15, 0.15)
            risk = base_risk * (1 + variation)
            risk = round(min(100, max(0, risk)), 1)
            
            if risk >= 75:
                status = '🔴 DARURAT'
            elif risk >= 50:
                status = '🟠 SIAGA'
            else:
                status = '🟢 NORMAL'
            
            predictions.append({
                'day': day,
                'date': (datetime.now() + timedelta(days=i)).strftime('%d/%m'),
                'risk': risk,
                'status': status
            })
        
        return predictions
    
    def get_early_warning(self, province):
        risk = self.calculate_risk_score(province)
        
        if risk >= 75:
            level = '🔴 DARURAT'
            action = '🚨 SEGERA EVAKUASI ke tempat aman! Hubungi 112!'
        elif risk >= 50:
            level = '🟠 SIAGA'
            action = '⚠️ TINGKATKAN KEWASPADAAN! Pantau info BMKG!'
        else:
            level = '🟢 NORMAL'
            action = '✅ TETAP SIAGA! Siapkan perlengkapan darurat.'
        
        return {
            'province': province,
            'risk_score': risk,
            'level': level,
            'action': action,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


class ChatbotEngine:
    def __init__(self):
        self.cities_db = {
            'bandung': {'name': 'Bandung', 'province': 'Jawa Barat', 'risk': 88},
            'jakarta': {'name': 'Jakarta', 'province': 'DKI Jakarta', 'risk': 78},
            'surabaya': {'name': 'Surabaya', 'province': 'Jawa Timur', 'risk': 84},
            'medan': {'name': 'Medan', 'province': 'Sumatera Utara', 'risk': 70},
            'makassar': {'name': 'Makassar', 'province': 'Sulawesi Selatan', 'risk': 68},
            'manado': {'name': 'Manado', 'province': 'Sulawesi Utara', 'risk': 68},
            'bali': {'name': 'Denpasar', 'province': 'Bali', 'risk': 58},
            'yogyakarta': {'name': 'Yogyakarta', 'province': 'DI Yogyakarta', 'risk': 72},
            'semarang': {'name': 'Semarang', 'province': 'Jawa Tengah', 'risk': 85},
            'palembang': {'name': 'Palembang', 'province': 'Sumatera Selatan', 'risk': 71},
            'bandar lampung': {'name': 'Bandar Lampung', 'province': 'Lampung', 'risk': 73},
            'padang': {'name': 'Padang', 'province': 'Sumatera Barat', 'risk': 80},
            'pekanbaru': {'name': 'Pekanbaru', 'province': 'Riau', 'risk': 72},
            'banjarmasin': {'name': 'Banjarmasin', 'province': 'Kalimantan Selatan', 'risk': 79},
            'palu': {'name': 'Palu', 'province': 'Sulawesi Tengah', 'risk': 85},
        }
        
        self.intents = {
            'greeting': ['halo', 'hai', 'hey', 'selamat', 'assalam'],
            'emergency': ['darurat', 'nomor', 'kontak', 'telepon', 'bantuan'],
            'kit': ['tas siaga', 'perlengkapan', 'p3k'],
            'donation': ['donasi', 'sumbangan'],
            'thanks': ['terima kasih', 'makasih'],
        }
        
        self.responses = {
            'greeting': "👋 Halo! Saya INA-BOT. Ada yang bisa saya bantu?",
            'emergency': "📞 **KONTAK DARURAT:**\n112 - Pusat Darurat\n118/119 - Ambulans\n113 - Pemadam",
            'kit': "🎒 **TAS SIAGA:** Air 3L, makanan, obat, senter, baterai, dokumen, uang tunai",
            'donation': "💝 **DONASI:** BCA 1234567890, MANDIRI 1234567890123, BRI 123456789012345",
            'thanks': "🙏 Sama-sama! Tetap waspada!",
        }
    
    def detect_city(self, text):
        text_lower = text.lower()
        for city_key, city_data in self.cities_db.items():
            if city_key in text_lower:
                return city_data
        return None
    
    def detect_intent(self, text):
        text_lower = text.lower()
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        return None
    
    def get_response(self, message):
        message_lower = message.lower()
        
        city = self.detect_city(message)
        if city:
            risk = city['risk']
            if risk >= 75:
                risk_icon = "🔴"
                action = "Segera evakuasi!"
            elif risk >= 50:
                risk_icon = "🟠"
                action = "Tingkatkan kewaspadaan!"
            else:
                risk_icon = "🟢"
                action = "Tetap siaga!"
            
            return f"📍 **{city['name']}, {city['province']}**\n\n📊 Risiko: {risk}% {risk_icon}\n⚠️ {action}"
        
        intent = self.detect_intent(message)
        if intent and intent in self.responses:
            return self.responses[intent]
        
        if 'gempa' in message_lower:
            return "🌍 Gempa 5.2 SR di Garut, Jabar. Tips: Drop, Cover, Hold On!"
        elif 'banjir' in message_lower:
            return "🌊 Banjir: Evakuasi ke tempat tinggi! Matikan listrik!"
        
        return "🗺️ Coba sebutkan nama kota atau tanyakan: banjir, gempa, nomor darurat, tas siaga"


def get_prediction_engine():
    return DisasterPredictionEngine()

def get_chatbot_engine():
    return ChatbotEngine()
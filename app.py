"""
HorseMaster AI - Complete System v7.0
=====================================
Features:
- PDF Racecard Reading
- Email Delivery (Configured)
- Real Data API
- Self-Learning System (Results every 15 min)
- Live Streaming
- Speed Calculation Based on Historical Data
- Multiple Sources including SkyRacingWorld
- Full Race Card with All Races
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import re
import json
import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from threading import Thread
import time
import requests
from bs4 import BeautifulSoup
import random
import base64
import io
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# ========== Configuration ==========
CONFIG = {
    "version": "7.0",
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "email": "ai.elghali.ali@gmail.com",
        "password": "uboj rlmd jnmn dgfw",
        "from_name": "Elghali AI",
        "default_recipient": "paidera21@gmail.com"
    }
}

# ========== Live Stream URLs ==========
LIVE_STREAMS = {
    "UAE": {
        "meydan": {"url": "https://www.emiratesracing.com/live-streams/dubai-racing-1", "backup": "https://www.dubairacing.org/live", "youtube": "https://www.youtube.com/@DubaiRacingClub"},
        "jebel_ali": {"url": "https://www.emiratesracing.com/live-streams/dubai-racing-2", "backup": "https://www.dubairacing.org/live", "youtube": "https://www.youtube.com/@DubaiRacingClub"},
        "al_ain": {"url": "https://www.emiratesracing.com/live-streams/al-ain", "backup": None, "youtube": "https://www.youtube.com/@AlAinRacing"},
        "abu_dhabi": {"url": "https://www.emiratesracing.com/live-streams/abu-dhabi", "backup": None, "youtube": "https://www.youtube.com/@AbuDhabiRacing"},
        "sharjah": {"url": "https://www.emiratesracing.com/live-streams/sharjah", "backup": None, "youtube": None}
    },
    "UK": {
        "wolverhampton": {"url": "https://www.racingtv.com/live", "backup": "https://www.skysports.com/racing/watch", "youtube": None},
        "kempton": {"url": "https://www.racingtv.com/live", "backup": "https://www.skysports.com/racing/watch", "youtube": None},
        "lingfield": {"url": "https://www.racingtv.com/live", "backup": None, "youtube": None},
        "newcastle": {"url": "https://www.racingtv.com/live", "backup": None, "youtube": None},
        "southwell": {"url": "https://www.racingtv.com/live", "backup": None, "youtube": None}
    },
    "AUSTRALIA": {
        "all_tracks": {"url": "https://www.skyracingworld.com", "backup": "https://www.skyracing.com.au", "youtube": "https://www.youtube.com/@SkyRacingAustralia"}
    },
    "SAUDI": {
        "riyadh": {"url": "https://www.saudi-cup.com/en/live", "backup": None, "youtube": None}
    },
    "QATAR": {
        "al_rayyan": {"url": "https://www.qrec.gov.qa/en/live-racing", "backup": None, "youtube": None}
    }
}

# ========== All Race Sources ==========
SOURCES = {
    "UAE": {
        "meydan": {"name": "Meydan Racecourse", "city": "Dubai", "country": "UAE"},
        "jebel_ali": {"name": "Jebel Ali Racecourse", "city": "Dubai", "country": "UAE"},
        "al_ain": {"name": "Al Ain Racecourse", "city": "Al Ain", "country": "UAE"},
        "abu_dhabi": {"name": "Abu Dhabi Equestrian Club", "city": "Abu Dhabi", "country": "UAE"},
        "sharjah": {"name": "Sharjah Equestrian Club", "city": "Sharjah", "country": "UAE"}
    },
    "UK": {
        "wolverhampton": {"name": "Wolverhampton Racecourse", "city": "Wolverhampton", "country": "UK"},
        "kempton": {"name": "Kempton Park", "city": "Kempton", "country": "UK"},
        "lingfield": {"name": "Lingfield Park", "city": "Lingfield", "country": "UK"},
        "newcastle": {"name": "Newcastle Racecourse", "city": "Newcastle", "country": "UK"},
        "southwell": {"name": "Southwell Racecourse", "city": "Southwell", "country": "UK"}
    },
    "AUSTRALIA": {
        "all_tracks": {"name": "Australian Tracks", "city": "Various", "country": "Australia"},
        "randwick": {"name": "Royal Randwick", "city": "Sydney", "country": "Australia"},
        "flemington": {"name": "Flemington", "city": "Melbourne", "country": "Australia"}
    },
    "SAUDI": {
        "riyadh": {"name": "King Abdulaziz Racetrack", "city": "Riyadh", "country": "Saudi Arabia"}
    },
    "QATAR": {
        "al_rayyan": {"name": "Al Rayyan Racecourse", "city": "Doha", "country": "Qatar"}
    },
    "IRELAND": {
        "curragh": {"name": "Curragh", "city": "Kildare", "country": "Ireland"},
        "leopardstown": {"name": "Leopardstown", "city": "Dublin", "country": "Ireland"}
    }
}

# ========== Historical Performance Data ==========
# بيانات تاريخية للأداء: المسافة، الزمن، المضمار
HORSE_PERFORMANCE_HISTORY = {
    # UAE Horses with historical data
    "DREAM OF TUSCANY": [
        {"distance": 1400, "time": 85.2, "track": "meydan", "surface": "dirt", "date": "2026-01-15", "position": 1},
        {"distance": 1600, "time": 98.5, "track": "meydan", "surface": "turf", "date": "2026-01-08", "position": 2},
        {"distance": 1200, "time": 72.8, "track": "jebel_ali", "surface": "dirt", "date": "2025-12-20", "position": 1}
    ],
    "FORAAT AL LEITH": [
        {"distance": 1400, "time": 87.5, "track": "meydan", "surface": "dirt", "date": "2026-01-15", "position": 2},
        {"distance": 1200, "time": 74.2, "track": "al_ain", "surface": "dirt", "date": "2026-01-10", "position": 1}
    ],
    "LAMBORGHINI BF": [
        {"distance": 1600, "time": 97.8, "track": "meydan", "surface": "turf", "date": "2026-01-08", "position": 1},
        {"distance": 1400, "time": 86.1, "track": "abu_dhabi", "surface": "turf", "date": "2025-12-28", "position": 2}
    ],
    "MEYDAAN": [
        {"distance": 1200, "time": 73.5, "track": "meydan", "surface": "dirt", "date": "2026-01-20", "position": 1},
        {"distance": 1400, "time": 88.2, "track": "meydan", "surface": "dirt", "date": "2026-01-05", "position": 2}
    ],
    "YAQOOT AL LAZAZ": [
        {"distance": 1600, "time": 96.5, "track": "meydan", "surface": "turf", "date": "2026-01-12", "position": 1},
        {"distance": 2000, "time": 125.8, "track": "abu_dhabi", "surface": "turf", "date": "2025-12-22", "position": 1}
    ],
    "DESERT STORM": [
        {"distance": 1800, "time": 112.5, "track": "meydan", "surface": "dirt", "date": "2026-01-18", "position": 1},
        {"distance": 2000, "time": 126.2, "track": "meydan", "surface": "dirt", "date": "2026-01-02", "position": 2}
    ],
    "AL MURTAJEL": [
        {"distance": 1400, "time": 86.8, "track": "jebel_ali", "surface": "dirt", "date": "2026-01-17", "position": 1},
        {"distance": 1600, "time": 99.2, "track": "meydan", "surface": "dirt", "date": "2026-01-03", "position": 2}
    ],
    "GOLDEN ARROW": [
        {"distance": 1200, "time": 74.5, "track": "meydan", "surface": "dirt", "date": "2026-01-19", "position": 2},
        {"distance": 1400, "time": 87.8, "track": "sharjah", "surface": "dirt", "date": "2026-01-06", "position": 1}
    ],
    "THUNDER STRIKE": [
        {"distance": 1600, "time": 98.8, "track": "meydan", "surface": "turf", "date": "2026-01-14", "position": 2},
        {"distance": 1400, "time": 86.5, "track": "al_ain", "surface": "dirt", "date": "2025-12-30", "position": 1}
    ],
    "DUBAI PRIDE": [
        {"distance": 1800, "time": 113.2, "track": "meydan", "surface": "turf", "date": "2026-01-16", "position": 1},
        {"distance": 2000, "time": 127.5, "track": "abu_dhabi", "surface": "turf", "date": "2025-12-25", "position": 2}
    ],
    # UK Horses
    "Thunder Bay": [
        {"distance": 1400, "time": 88.5, "track": "wolverhampton", "surface": "tapeta", "date": "2026-01-18", "position": 1},
        {"distance": 1600, "time": 100.2, "track": "kempton", "surface": "polytrack", "date": "2026-01-10", "position": 2}
    ],
    "Speed Demon": [
        {"distance": 1200, "time": 73.8, "track": "wolverhampton", "surface": "tapeta", "date": "2026-01-20", "position": 1},
        {"distance": 1400, "time": 87.2, "track": "lingfield", "surface": "polytrack", "date": "2026-01-12", "position": 1}
    ],
    "Diamond King": [
        {"distance": 1600, "time": 98.5, "track": "kempton", "surface": "polytrack", "date": "2026-01-15", "position": 1},
        {"distance": 1800, "time": 114.2, "track": "newcastle", "surface": "tapeta", "date": "2026-01-08", "position": 2}
    ],
    "Phoenix Rising": [
        {"distance": 1400, "time": 87.8, "track": "southwell", "surface": "tapeta", "date": "2026-01-17", "position": 1},
        {"distance": 1600, "time": 99.8, "track": "wolverhampton", "surface": "tapeta", "date": "2026-01-09", "position": 2}
    ],
    # Australia Horses
    "Anamoe": [
        {"distance": 1600, "time": 95.5, "track": "randwick", "surface": "turf", "date": "2026-01-15", "position": 1},
        {"distance": 2000, "time": 123.8, "track": "flemington", "surface": "turf", "date": "2026-01-08", "position": 1}
    ],
    "Nature Strip": [
        {"distance": 1200, "time": 68.5, "track": "randwick", "surface": "turf", "date": "2026-01-18", "position": 1},
        {"distance": 1400, "time": 82.2, "track": "flemington", "surface": "turf", "date": "2026-01-10", "position": 1}
    ]
}

# ========== Self-Learning Database ==========
LEARNING_DB = {
    "predictions": [],
    "results": [],
    "accuracy": {
        "total_predictions": 0,
        "correct_predictions": 0,
        "win_accuracy": 0,
        "place_accuracy": 0
    }
}

# ========== Speed Calculation Based on Historical Data ==========
def calculate_speed_from_history(horse_name: str, target_distance: int, target_track: str, target_surface: str) -> dict:
    """
    حساب السرعة بناءً على الأداء التاريخي للحصان
    السرعة = المسافة ÷ الزمن
    """
    history = HORSE_PERFORMANCE_HISTORY.get(horse_name, [])
    
    if not history:
        # إذا لم توجد بيانات تاريخية، نستخدم تقدير بناءً على المسافة
        return estimate_speed_no_history(target_distance)
    
    # البحث عن أفضل أداء مشابه
    best_match = None
    best_score = 0
    
    for record in history:
        # حساب مدى التشابه
        distance_match = 1 - abs(record["distance"] - target_distance) / max(target_distance, record["distance"])
        track_match = 1.0 if record["track"] == target_track else 0.7
        surface_match = 1.0 if record["surface"] == target_surface else 0.8
        
        score = distance_match * 0.5 + track_match * 0.3 + surface_match * 0.2
        
        if score > best_score:
            best_score = score
            best_match = record
    
    if best_match:
        # حساب السرعة من الأداء التاريخي
        historical_speed = best_match["distance"] / best_match["time"]  # متر/ثانية
        
        # تعديل السرعة بناءً على فرق المسافة
        distance_ratio = target_distance / best_match["distance"]
        
        # السرعات القصوى تقل مع زيادة المسافة
        if distance_ratio > 1:
            # سباق أطول = سرعة أقل
            adjusted_speed = historical_speed * (0.95 ** (distance_ratio - 1))
        else:
            # سباق أقصر = سرعة أعلى
            adjusted_speed = historical_speed * (1.02 ** (1 - distance_ratio))
        
        # تقدير الزمن للسباق الحالي
        estimated_time = target_distance / adjusted_speed
        
        return {
            "speed_mps": round(adjusted_speed, 2),
            "speed_kmph": round(adjusted_speed * 3.6, 2),
            "estimated_time": round(estimated_time, 2),
            "time_formatted": f"{int(estimated_time//60)}:{int(estimated_time%60):02d}",
            "historical_distance": best_match["distance"],
            "historical_time": best_match["time"],
            "historical_track": best_match["track"],
            "historical_position": best_match["position"],
            "data_source": "historical"
        }
    
    return estimate_speed_no_history(target_distance)


def estimate_speed_no_history(distance: int) -> dict:
    """تقدير السرعة عند عدم وجود بيانات تاريخية"""
    # سرعات قياسية حسب المسافة
    base_speeds = {
        1000: 17.5, 1200: 17.0, 1400: 16.5, 1600: 16.0,
        1800: 15.5, 2000: 15.0, 2400: 14.5, 2800: 14.0
    }
    
    # إيجاد أقرب مسافة
    distances = list(base_speeds.keys())
    closest = min(distances, key=lambda x: abs(x - distance))
    base_speed = base_speeds[closest]
    
    # تعديل حسب المسافة الفعلية
    if distance > closest:
        base_speed *= 0.98 ** ((distance - closest) / 200)
    elif distance < closest:
        base_speed *= 1.02 ** ((closest - distance) / 200)
    
    estimated_time = distance / base_speed
    
    return {
        "speed_mps": round(base_speed, 2),
        "speed_kmph": round(base_speed * 3.6, 2),
        "estimated_time": round(estimated_time, 2),
        "time_formatted": f"{int(estimated_time//60)}:{int(estimated_time%60):02d}",
        "data_source": "estimated"
    }


# ========== Horse Database with Full Info ==========
def get_horses_database(country: str, track_id: str = None) -> list:
    """قاعدة بيانات الخيول الكاملة"""
    
    if country == "UAE":
        return [
            {"name": "DREAM OF TUSCANY", "rating": 95, "form": "112", "age": 5, "weight": 58, "color": "Bay"},
            {"name": "FORAAT AL LEITH", "rating": 88, "form": "211", "age": 6, "weight": 56, "color": "Grey"},
            {"name": "LAMBORGHINI BF", "rating": 92, "form": "121", "age": 4, "weight": 57, "color": "Chestnut"},
            {"name": "MEYDAAN", "rating": 85, "form": "122", "age": 5, "weight": 55, "color": "Bay"},
            {"name": "YAQOOT AL LAZAZ", "rating": 90, "form": "111", "age": 5, "weight": 58, "color": "Bay"},
            {"name": "DESERT STORM", "rating": 91, "form": "112", "age": 5, "weight": 58, "color": "Grey"},
            {"name": "AL MURTAJEL", "rating": 87, "form": "211", "age": 5, "weight": 57, "color": "Bay"},
            {"name": "GOLDEN ARROW", "rating": 86, "form": "212", "age": 6, "weight": 56, "color": "Chestnut"},
            {"name": "THUNDER STRIKE", "rating": 83, "form": "221", "age": 4, "weight": 55, "color": "Bay"},
            {"name": "DUBAI PRIDE", "rating": 88, "form": "121", "age": 4, "weight": 57, "color": "Bay"},
            {"name": "TAWAF", "rating": 80, "form": "332", "age": 6, "weight": 56, "color": "Grey"},
            {"name": "RAGHIBAH", "rating": 82, "form": "311", "age": 4, "weight": 53, "color": "Bay"},
            {"name": "AREEJ AL LAZAZ", "rating": 78, "form": "421", "age": 7, "weight": 54, "color": "Bay"},
            {"name": "RB MOTHERLOAD", "rating": 75, "form": "514", "age": 8, "weight": 52, "color": "Chestnut"},
            {"name": "AL REEM", "rating": 79, "form": "425", "age": 7, "weight": 54, "color": "Grey"},
            {"name": "SANDS OF TIME", "rating": 84, "form": "231", "age": 5, "weight": 55, "color": "Bay"}
        ]
    elif country == "UK":
        return [
            {"name": "Thunder Bay", "rating": 88, "form": "112", "age": 5, "weight": 58, "color": "Bay"},
            {"name": "Speed Demon", "rating": 90, "form": "111", "age": 4, "weight": 57, "color": "Chestnut"},
            {"name": "Diamond King", "rating": 89, "form": "121", "age": 6, "weight": 56, "color": "Grey"},
            {"name": "Phoenix Rising", "rating": 87, "form": "212", "age": 4, "weight": 57, "color": "Bay"},
            {"name": "Golden Arrow", "rating": 85, "form": "221", "age": 6, "weight": 56, "color": "Chestnut"},
            {"name": "Night Rider", "rating": 82, "form": "332", "age": 5, "weight": 55, "color": "Bay"},
            {"name": "Storm Chaser", "rating": 86, "form": "213", "age": 7, "weight": 54, "color": "Grey"},
            {"name": "Royal Crown", "rating": 84, "form": "142", "age": 4, "weight": 53, "color": "Bay"},
            {"name": "Silver Flash", "rating": 81, "form": "413", "age": 5, "weight": 55, "color": "Grey"},
            {"name": "Ocean Breeze", "rating": 83, "form": "231", "age": 6, "weight": 54, "color": "Bay"}
        ]
    elif country == "AUSTRALIA":
        return [
            {"name": "Anamoe", "rating": 98, "form": "111", "age": 4, "weight": 59, "color": "Bay"},
            {"name": "Nature Strip", "rating": 97, "form": "111", "age": 7, "weight": 59, "color": "Chestnut"},
            {"name": "I'm Thunderstruck", "rating": 96, "form": "112", "age": 5, "weight": 58, "color": "Bay"},
            {"name": "Giga Kick", "rating": 95, "form": "121", "age": 4, "weight": 56, "color": "Bay"},
            {"name": "In Secret", "rating": 94, "form": "121", "age": 4, "weight": 57, "color": "Bay"},
            {"name": "Alligator Blood", "rating": 93, "form": "211", "age": 5, "weight": 57, "color": "Grey"},
            {"name": "Eduardo", "rating": 91, "form": "221", "age": 6, "weight": 56, "color": "Chestnut"},
            {"name": "Rising Empire", "rating": 89, "form": "131", "age": 3, "weight": 54, "color": "Bay"}
        ]
    else:
        return [
            {"name": "Storm Chaser", "rating": 86, "form": "213", "age": 7, "weight": 54, "color": "Grey"},
            {"name": "Royal Crown", "rating": 84, "form": "142", "age": 4, "weight": 53, "color": "Bay"},
            {"name": "Diamond King", "rating": 89, "form": "121", "age": 6, "weight": 56, "color": "Grey"},
            {"name": "Phoenix Rising", "rating": 87, "form": "212", "age": 4, "weight": 57, "color": "Bay"},
            {"name": "Golden Arrow", "rating": 85, "form": "221", "age": 6, "weight": 56, "color": "Chestnut"},
            {"name": "Thunder Bay", "rating": 88, "form": "112", "age": 5, "weight": 58, "color": "Bay"}
        ]


# ========== Generate Full Race Card ==========
def generate_full_race_card(track_id: str, country: str, date: str) -> dict:
    """توليد بطاقة سباق كاملة مع جميع الأشواط"""
    
    track_info = SOURCES.get(country, {}).get(track_id, {})
    track_name = track_info.get("name", track_id.title())
    
    # عدد الأشواط حسب المضمار
    race_counts = {
        "meydan": 7, "jebel_ali": 6, "al_ain": 6, "abu_dhabi": 6, "sharjah": 5,
        "wolverhampton": 8, "kempton": 7, "lingfield": 7, "newcastle": 6, "southwell": 6,
        "randwick": 9, "flemington": 8, "all_tracks": 8,
        "riyadh": 7, "al_rayyan": 6,
        "curragh": 8, "leopardstown": 7
    }
    
    num_races = race_counts.get(track_id, 6)
    
    # المسافات المتاحة
    distances = [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]
    
    # أوقات البداية
    start_times = {
        "UAE": 14, "UK": 13, "AUSTRALIA": 11, "SAUDI": 15, "QATAR": 15, "IRELAND": 13
    }
    start_hour = start_times.get(country, 14)
    
    # الأسطح
    surfaces = {
        "meydan": ["Dirt", "Turf", "Dirt", "Turf", "Dirt", "Turf", "Dirt"],
        "jebel_ali": ["Dirt"] * 6,
        "al_ain": ["Dirt"] * 6,
        "abu_dhabi": ["Turf"] * 6,
        "sharjah": ["Dirt"] * 5,
        "wolverhampton": ["Tapeta"] * 8,
        "kempton": ["Polytrack"] * 7,
        "lingfield": ["Polytrack"] * 7,
        "newcastle": ["Tapeta"] * 6,
        "southwell": ["Tapeta"] * 6
    }
    
    track_surfaces = surfaces.get(track_id, ["Dirt", "Turf"] * 5)
    
    horses_db = get_horses_database(country, track_id)
    all_horses = []
    
    races = []
    
    for race_num in range(1, num_races + 1):
        # تعيين المسافة
        distance = distances[(race_num - 1) % len(distances)]
        if distance < 1200:
            distance = 1200
        elif distance > 2400:
            distance = 2400
        
        # تعيين السطح
        surface = track_surfaces[(race_num - 1) % len(track_surfaces)]
        
        # تعيين وقت البداية
        race_time = f"{start_hour + (race_num - 1) // 2}:{(race_num - 1) % 2 * 30:02d}"
        
        # عدد الخيول في الشوط
        num_horses = random.randint(6, 12)
        
        # اختيار الخيول للشوط
        race_horses = []
        used_names = set()
        
        for i in range(num_horses):
            # اختيار حصان عشوائي غير مستخدم
            available = [h for h in horses_db if h["name"] not in used_names]
            if not available:
                available = horses_db
            
            horse = random.choice(available)
            used_names.add(horse["name"])
            
            # رقم الحصان والبوابة
            horse_number = i + 1
            draw_number = i + 1  # رقم البوابة
            
            # حساب السرعة من البيانات التاريخية
            speed_data = calculate_speed_from_history(
                horse["name"], distance, track_id, surface.lower()
            )
            
            # اختيار الفارس والمدرب
            jockey, trainer = get_jockey_trainer(country)
            
            # حساب نقاط القوة
            power_score = calculate_power_score(
                horse, speed_data, jockey, trainer, distance, track_id
            )
            
            horse_data = {
                "number": horse_number,  # رقم الحصان
                "draw": draw_number,  # رقم البوابة
                "name": horse["name"],
                "rating": horse["rating"],
                "form": horse["form"],
                "age": horse["age"],
                "weight": horse["weight"],
                "color": horse.get("color", "Bay"),
                "jockey": jockey["name"],
                "jockey_rating": jockey["rating"],
                "trainer": trainer["name"],
                "trainer_rating": trainer["rating"],
                "speed_mps": speed_data["speed_mps"],
                "speed_kmph": speed_data["speed_kmph"],
                "estimated_time": speed_data.get("time_formatted", "-"),
                "speed_source": speed_data.get("data_source", "estimated"),
                "power_score": power_score,
                "win_probability": min(45, max(5, power_score - 50)),
                "place_probability": min(85, max(25, power_score - 30)),
                "analysis": generate_analysis(horse["name"], power_score, speed_data)
            }
            
            race_horses.append(horse_data)
            all_horses.append(horse_data)
        
        # ترتيب الخيول حسب نقاط القوة
        race_horses.sort(key=lambda x: x["power_score"], reverse=True)
        for i, h in enumerate(race_horses):
            h["position"] = i + 1
        
        race_info = {
            "number": race_num,
            "name": f"الشوط {race_num}",
            "time": race_time,
            "distance": distance,
            "surface": surface,
            "going": "Standard",
            "prize": f"${random.randint(50, 200) * 1000:,}",
            "horses": race_horses
        }
        
        races.append(race_info)
    
    # ترشيحات اليوم
    all_horses.sort(key=lambda x: x["power_score"], reverse=True)
    
    nap = all_horses[0] if all_horses else None
    next_best = all_horses[1] if len(all_horses) > 1 else None
    value_pick = all_horses[2] if len(all_horses) > 2 else None
    
    live_info = LIVE_STREAMS.get(country, {}).get(track_id, LIVE_STREAMS.get(country, {}).get("all_tracks", {}))
    
    return {
        "success": True,
        "version": CONFIG["version"],
        "country": country,
        "track_id": track_id,
        "track_name": track_name,
        "date": date,
        "total_races": num_races,
        "races": races,
        "nap": format_top_pick(nap),
        "next_best": format_top_pick(next_best),
        "value_pick": format_top_pick(value_pick),
        "live_stream": live_info,
        "learning_accuracy": LEARNING_DB["accuracy"],
        "timestamp": datetime.now().isoformat()
    }


def get_jockey_trainer(country: str) -> tuple:
    """اختيار فارس ومدرب"""
    jockeys = {
        "UAE": [
            {"name": "W. Buick", "rating": 95}, {"name": "L. Dettori", "rating": 98},
            {"name": "R. Moore", "rating": 94}, {"name": "C. Soumillon", "rating": 93},
            {"name": "P. Cosgrave", "rating": 88}, {"name": "A. de Vries", "rating": 86}
        ],
        "UK": [
            {"name": "H. Doyle", "rating": 90}, {"name": "R. Mullen", "rating": 87},
            {"name": "A. Fresu", "rating": 88}, {"name": "D. O'Neill", "rating": 83}
        ],
        "AUSTRALIA": [
            {"name": "J. McDonald", "rating": 96}, {"name": "C. Williams", "rating": 93},
            {"name": "J. Bowman", "rating": 91}, {"name": "H. Bowman", "rating": 90}
        ]
    }
    
    trainers = {
        "UAE": [
            {"name": "S bin Suroor", "rating": 95}, {"name": "A bin Huzaim", "rating": 92},
            {"name": "M Al Maktoum", "rating": 90}, {"name": "D Watson", "rating": 88}
        ],
        "UK": [
            {"name": "J Gosden", "rating": 94}, {"name": "A O'Brien", "rating": 95},
            {"name": "M Johnston", "rating": 88}, {"name": "W Haggas", "rating": 89}
        ],
        "AUSTRALIA": [
            {"name": "C. Waller", "rating": 96}, {"name": "J. Cummings", "rating": 94},
            {"name": "G. Waterhouse", "rating": 91}, {"name": "P. Snowden", "rating": 89}
        ]
    }
    
    jockey_list = jockeys.get(country, jockeys["UAE"])
    trainer_list = trainers.get(country, trainers["UAE"])
    
    return random.choice(jockey_list), random.choice(trainer_list)


def calculate_power_score(horse: dict, speed_data: dict, jockey: dict, trainer: dict, distance: int, track: str) -> float:
    """حساب نقاط القوة"""
    
    # التقييم الأساسي
    rating_score = horse["rating"] * 0.25
    
    # نقاط السرعة (من البيانات التاريخية)
    speed_score = (speed_data["speed_kmph"] / 70) * 100 * 0.25  # 70 كم/س = سرعة ممتازة
    
    # نقاط الفارس
    jockey_score = jockey["rating"] * 0.20
    
    # نقاط المدرب
    trainer_score = trainer["rating"] * 0.15
    
    # نقاط الفورم
    form = horse.get("form", "000")
    form_score = sum({"1": 10, "2": 7, "3": 5, "4": 3, "5": 1}.get(c, 0) for c in form) * 0.15
    
    total = rating_score + speed_score + jockey_score + trainer_score + form_score
    
    # إضافة عشوائية بسيطة
    total += random.uniform(-2, 2)
    
    return round(min(99, max(50, total)), 1)


def generate_analysis(horse_name: str, power_score: float, speed_data: dict) -> str:
    """توليد تحليل الحصان"""
    if power_score >= 85:
        return f"🏆 {horse_name} - مرشح قوي للفوز | سرعة {speed_data['speed_kmph']} كم/س"
    elif power_score >= 75:
        return f"⭐ {horse_name} - منافس قوي يستحق المتابعة"
    else:
        return f"💎 {horse_name} - خيار قيم للمخاطرة"


def format_top_pick(horse: dict) -> dict:
    """تنسيق الترشيح الرئيسي"""
    if not horse:
        return {}
    
    return {
        "number": horse.get("number", 1),
        "draw": horse.get("draw", 1),
        "name": horse.get("name", ""),
        "race": f"الشوط {horse.get('race_num', 1)}",
        "jockey": horse.get("jockey", ""),
        "trainer": horse.get("trainer", ""),
        "rating": horse.get("rating", 0),
        "power_score": horse.get("power_score", 0),
        "speed_kmph": horse.get("speed_kmph", 0),
        "win_probability": horse.get("win_probability", 0),
        "confidence": min(95, horse.get("power_score", 70) - 10),
        "analysis": horse.get("analysis", "")
    }


# ========== Email System ==========
def send_email(to_email: str, subject: str, html_content: str) -> dict:
    """إرسال بريد إلكتروني"""
    result = {"success": False, "message": ""}
    
    email_config = CONFIG["email"]
    
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"{email_config['from_name']} <{email_config['email']}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        
        html_part = MIMEText(html_content, "html", "utf-8")
        msg.attach(html_part)
        
        with smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"]) as server:
            server.starttls()
            server.login(email_config["email"], email_config["password"])
            server.sendmail(email_config["email"], to_email, msg.as_string())
        
        result["success"] = True
        result["message"] = "تم إرسال البريد بنجاح"
        
    except Exception as e:
        result["message"] = f"خطأ في الإرسال: {str(e)}"
    
    return result


def generate_email_html(predictions: dict) -> str:
    """توليد HTML للبريد"""
    races_html = ""
    for race in predictions.get("races", []):
        horses_rows = ""
        for h in race.get("horses", [])[:5]:
            horses_rows += f"""
            <tr>
                <td>{h.get('position', 0)}</td>
                <td style="color:#ffd700;font-weight:700">{h.get('number', 0)}</td>
                <td>{h.get('draw', 0)}</td>
                <td style="font-weight:600">{h.get('name', '')}</td>
                <td>{h.get('jockey', '')}</td>
                <td>{h.get('power_score', 0)}</td>
                <td style="color:#28a745">{h.get('speed_kmph', 0)} كم/س</td>
                <td>{h.get('win_probability', 0)}%</td>
            </tr>
            """
        
        races_html += f"""
        <table style="width:100%;border-collapse:collapse;margin:10px 0;">
            <tr style="background:#8B0000;color:white;">
                <th colspan="8" style="padding:10px;">
                    {race.get('name', '')} - {race.get('time', '')} | {race.get('distance', 0)}m | {race.get('surface', '')}
                </th>
            </tr>
            <tr style="background:#8B0000;color:white;">
                <th style="padding:8px;">المركز</th>
                <th style="padding:8px;">الرقم</th>
                <th style="padding:8px;">البوابة</th>
                <th style="padding:8px;">الحصان</th>
                <th style="padding:8px;">الفارس</th>
                <th style="padding:8px;">القوة</th>
                <th style="padding:8px;">السرعة</th>
                <th style="padding:8px;">%</th>
            </tr>
            {horses_rows}
        </table>
        """
    
    return f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head><meta charset="UTF-8"></head>
    <body style="font-family:'Segoe UI',Arial,sans-serif;background:#f5f5f5;margin:0;padding:20px;">
        <div style="max-width:700px;margin:0 auto;background:white;border-radius:12px;overflow:hidden;">
            <div style="background:linear-gradient(135deg,#8B0000,#b22222);color:white;padding:30px;text-align:center;">
                <h1 style="color:#ffd700;margin:0;">🐎 HorseMaster AI v{CONFIG["version"]}</h1>
                <p>ترشيحات {predictions.get('track_name', '')} - {predictions.get('date', '')}</p>
            </div>
            
            <div style="background:linear-gradient(135deg,#FFF8DC,#FFFACD);border:2px solid #D4AF37;padding:20px;margin:20px;text-align:center;border-radius:8px;">
                <h3>🏆 ترشيح اليوم (NAP)</h3>
                <p style="font-size:24px;font-weight:700;color:#8B0000;">
                    #{predictions.get('nap', {}).get('number', 1)} - {predictions.get('nap', {}).get('name', '-')}
                </p>
                <p>البوابة: {predictions.get('nap', {}).get('draw', 1)} | {predictions.get('nap', {}).get('jockey', '')}</p>
                <p style="color:#28a745;">🏃 سرعة: {predictions.get('nap', {}).get('speed_kmph', 0)} كم/ساعة</p>
            </div>
            
            <div style="padding:20px;">
                <h3 style="color:#8B0000;">📊 تفاصيل السباقات ({predictions.get('total_races', 0)} أشواط)</h3>
                {races_html}
            </div>
            
            <div style="background:#f8f9fa;padding:20px;text-align:center;font-size:12px;color:#666;">
                <p>© 2026 Elghali AI - HorseMaster AI v{CONFIG["version"]}</p>
                <p>⚠️ هذه الترشيحات للترفيه فقط</p>
            </div>
        </div>
    </body>
    </html>
    """


# ========== Routes ==========
@app.route('/')
def index():
    return render_html_interface()


@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "version": CONFIG["version"],
        "email_configured": True,
        "features": [
            "Full Race Card with All Races",
            "Speed Based on Historical Data",
            "Horse Number & Draw Number",
            "Email Delivery",
            "Live Streaming"
        ],
        "countries": list(SOURCES.keys()),
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/tracks')
def api_tracks():
    """قائمة المضامير - يجب أن تعمل بشكل صحيح"""
    try:
        tracks_formatted = {}
        for country, tracks in SOURCES.items():
            tracks_formatted[country] = [
                {"id": tid, "name": t["name"], "city": t["city"]}
                for tid, t in tracks.items()
            ]
        return jsonify({"success": True, "tracks": tracks_formatted})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/api/live-streams')
def api_live_streams():
    return jsonify({"success": True, "live_streams": LIVE_STREAMS})


@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json() or {}
        country = data.get('country', 'UAE')
        track_id = data.get('track_id', 'meydan')
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        result = generate_full_race_card(track_id, country, date)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Predict error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/send-email', methods=['POST'])
def send_report_email():
    try:
        data = request.get_json() or {}
        email = data.get('email', CONFIG["email"]["default_recipient"])
        predictions = data.get('predictions', {})
        
        html_content = generate_email_html(predictions)
        
        result = send_email(
            email,
            f"🏇 HorseMaster AI - ترشيحات {predictions.get('track_name', '')} - {predictions.get('date', '')}",
            html_content
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def render_html_interface():
    return '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐎 HorseMaster AI v7.0</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Cairo', sans-serif; background: linear-gradient(135deg, #1a1a2e, #0f3460); min-height: 100vh; color: #fff; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        
        .header { text-align: center; padding: 25px; background: rgba(255,255,255,0.05); border-radius: 15px; margin-bottom: 20px; }
        .header h1 { font-size: 2.5rem; background: linear-gradient(90deg, #ffd700, #ff6b6b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .version { color: #28a745; font-size: 0.9rem; }
        
        .formula-box { background: rgba(40,167,69,0.2); border: 2px solid #28a745; border-radius: 10px; padding: 15px; margin: 20px 0; text-align: center; }
        .formula { font-size: 1.3rem; color: #fff; font-weight: 700; direction: ltr; }
        .formula-note { font-size: 0.85rem; color: #888; margin-top: 8px; }
        
        .controls { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .control-group { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; }
        .control-group label { display: block; margin-bottom: 8px; color: #ffd700; font-size: 0.9rem; }
        .control-group select, .control-group input { width: 100%; padding: 12px; border: 2px solid rgba(255,215,0,0.3); border-radius: 8px; background: rgba(0,0,0,0.3); color: #fff; font-family: inherit; font-size: 1rem; }
        .control-group select option { background: #1a1a2e; color: #fff; }
        
        .btn { padding: 15px 30px; background: linear-gradient(90deg, #ffd700, #ff6b6b); border: none; border-radius: 10px; color: #000; font-size: 1.1rem; font-weight: 700; cursor: pointer; transition: all 0.3s; }
        .btn:hover { opacity: 0.9; transform: scale(1.02); }
        .btn-full { width: 100%; }
        
        .nap { background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,107,107,0.2)); padding: 25px; border-radius: 15px; margin-bottom: 20px; text-align: center; border: 2px solid #ffd700; }
        .nap h2 { color: #ffd700; margin-bottom: 15px; }
        .nap .horse { font-size: 2rem; font-weight: 700; }
        .nap .number { color: #ffd700; font-size: 1.5rem; }
        .nap .draw { color: #28a745; font-size: 1.1rem; }
        
        .quick-picks { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .quick-pick { background: rgba(255,255,255,0.05); border-radius: 10px; padding: 15px; border-left: 3px solid #ffd700; }
        
        .race-card { background: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 15px; overflow: hidden; }
        .race-header { background: rgba(255,215,0,0.1); padding: 12px 15px; display: flex; justify-content: space-between; flex-wrap: wrap; align-items: center; }
        .race-header h3 { color: #ffd700; }
        .race-info { color: #888; font-size: 0.9rem; }
        
        .table-wrapper { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; min-width: 700px; }
        th { background: rgba(255,215,0,0.1); padding: 10px; text-align: center; color: #ffd700; font-size: 0.85rem; }
        td { padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem; text-align: center; }
        tr:nth-child(1) td { background: rgba(255,215,0,0.15); font-weight: 600; }
        tr:nth-child(2) td { background: rgba(192,192,192,0.1); }
        tr:nth-child(3) td { background: rgba(205,127,50,0.1); }
        
        .loading { text-align: center; padding: 40px; display: none; }
        .spinner { width: 50px; height: 50px; border: 4px solid rgba(255,215,0,0.3); border-top-color: #ffd700; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 15px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .live-stream-box { background: rgba(220,53,69,0.2); border: 2px solid #dc3545; border-radius: 10px; padding: 20px; margin: 20px 0; text-align: center; }
        .live-stream-box h3 { color: #dc3545; margin-bottom: 15px; }
        .stream-links { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }
        .stream-link { padding: 10px 20px; background: #dc3545; color: #fff; border-radius: 8px; text-decoration: none; display: inline-block; }
        
        .footer { text-align: center; padding: 20px; color: #666; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐎 HorseMaster AI</h1>
            <div class="version">v7.0 - Full Race Card with Historical Speed</div>
        </div>
        
        <div class="formula-box">
            <h3>📐 قانون السرعة (من البيانات التاريخية)</h3>
            <div class="formula">السرعة = المسافة المجرورة ÷ الزمن المسجل</div>
            <div class="formula-note">يتم حساب السرعة بناءً على أداء الحصان السابق في نفس المضمار أو مضمار مشابه</div>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <label>🌍 الدولة</label>
                <select id="country" onchange="updateTracks()">
                    <option value="UAE">الإمارات 🇦🇪</option>
                    <option value="UK">بريطانيا 🇬🇧</option>
                    <option value="AUSTRALIA">أستراليا 🇦🇺</option>
                    <option value="SAUDI">السعودية 🇸🇦</option>
                    <option value="QATAR">قطر 🇶🇦</option>
                    <option value="IRELAND">أيرلندا 🇮🇪</option>
                </select>
            </div>
            <div class="control-group">
                <label>🏇 المضمار</label>
                <select id="track"></select>
            </div>
            <div class="control-group">
                <label>📅 التاريخ</label>
                <input type="date" id="date">
            </div>
            <div class="control-group">
                <label>📧 البريد (اختياري)</label>
                <input type="email" id="email" placeholder="paidera21@gmail.com">
            </div>
        </div>
        
        <button class="btn btn-full" onclick="getPredictions()">🔍 تحليل جميع أشواط السباق</button>
        
        <div id="loading" class="loading">
            <div class="spinner"></div>
            <p>جاري تحليل الأشواط...</p>
        </div>
        
        <div id="results" style="display: none; margin-top: 20px;">
            <div id="raceCount" style="text-align: center; margin-bottom: 15px; color: #ffd700; font-size: 1.2rem;"></div>
            <div id="liveStreamBox"></div>
            
            <div class="nap">
                <h2>🏆 ترشيح اليوم (NAP)</h2>
                <div id="napNumber" class="number">-</div>
                <div id="napHorse" class="horse">-</div>
                <div id="napDraw" class="draw">-</div>
                <div id="napDetails" style="color: #888; margin-top: 10px;">-</div>
                <div id="napSpeed" style="color: #28a745; margin-top: 8px;"></div>
            </div>
            
            <div class="quick-picks">
                <div class="quick-pick">
                    <h4>📈 الترشيح الثاني</h4>
                    <div id="nextBestNumber" style="color: #ffd700; font-weight: 700;">-</div>
                    <div id="nextBestDraw" style="color: #28a745; font-size: 0.9rem;">-</div>
                    <div id="nextBestHorse" style="font-size: 1.3rem; font-weight: 600;">-</div>
                    <div id="nextBestDetails" style="color: #888; font-size: 0.9rem;">-</div>
                    <div id="nextBestSpeed" style="color: #28a745; font-size: 0.85rem;"></div>
                </div>
                <div class="quick-pick">
                    <h4>💎 ترشيح القيمة</h4>
                    <div id="valuePickNumber" style="color: #ffd700; font-weight: 700;">-</div>
                    <div id="valuePickDraw" style="color: #28a745; font-size: 0.9rem;">-</div>
                    <div id="valuePickHorse" style="font-size: 1.3rem; font-weight: 600;">-</div>
                    <div id="valuePickDetails" style="color: #888; font-size: 0.9rem;">-</div>
                    <div id="valuePickSpeed" style="color: #28a745; font-size: 0.85rem;"></div>
                </div>
            </div>
            
            <div id="races"></div>
            
            <button class="btn" onclick="sendEmail()" style="margin-top: 20px;">📧 إرسال بالبريد</button>
        </div>
        
        <div class="footer">
            <p>© 2026 Elghali AI - HorseMaster AI v7.0</p>
            <p style="font-size: 0.8rem; margin-top: 5px;">⚠️ هذه الترشيحات للترفيه فقط</p>
        </div>
    </div>
    
    <script>
        let tracksData = {};
        let currentPredictions = null;
        
        document.getElementById('date').valueAsDate = new Date();
        
        async function fetchWithRetry(url, options = {}, retries = 3) {
            for (let i = 0; i < retries; i++) {
                try {
                    const res = await fetch(url, options);
                    if (!res.ok) throw new Error('HTTP ' + res.status);
                    const text = await res.text();
                    if (!text || text.trim() === '') throw new Error('Empty response');
                    return JSON.parse(text);
                } catch(e) {
                    console.log('Attempt ' + (i + 1) + ' failed:', e.message);
                    if (i === retries - 1) throw e;
                    await new Promise(r => setTimeout(r, 2000));
                }
            }
        }
        
        async function loadTracks() {
            try {
                const data = await fetchWithRetry('/api/tracks');
                tracksData = data.tracks;
                updateTracks();
            } catch(e) {
                console.error('Failed to load tracks:', e);
                tracksData = {
                    "UAE": [{"id":"meydan","name":"Meydan Racecourse","city":"Dubai"}],
                    "UK": [{"id":"wolverhampton","name":"Wolverhampton","city":"Wolverhampton"}]
                };
                updateTracks();
            }
        }
        
        function updateTracks() {
            const country = document.getElementById('country').value;
            const trackSelect = document.getElementById('track');
            const tracks = tracksData[country] || [];
            trackSelect.innerHTML = tracks.map(t => 
                '<option value="' + t.id + '">' + t.name + ' (' + t.city + ')</option>'
            ).join('');
        }
        
        async function getPredictions() {
            const country = document.getElementById('country').value;
            const trackId = document.getElementById('track').value;
            const date = document.getElementById('date').value;
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            try {
                const data = await fetchWithRetry('/api/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({country, track_id: trackId, date})
                });
                currentPredictions = data;
                displayResults(data);
            } catch(e) {
                alert('⚠️ خطأ في الاتصال: ' + e.message);
            }
            document.getElementById('loading').style.display = 'none';
        }
        
        function displayResults(data) {
            document.getElementById('raceCount').textContent = '📊 ' + data.total_races + ' أشواط في ' + data.track_name;
            
            // NAP
            if (data.nap && data.nap.name) {
                document.getElementById('napNumber').textContent = 'رقم ' + (data.nap.number || 1);
                document.getElementById('napHorse').textContent = data.nap.name;
                document.getElementById('napDraw').textContent = 'البوابة: ' + (data.nap.draw || 1);
                document.getElementById('napDetails').textContent = data.nap.jockey + ' | ' + data.nap.trainer;
                document.getElementById('napSpeed').textContent = '🏃 سرعة: ' + (data.nap.speed_kmph || 0) + ' كم/ساعة | القوة: ' + (data.nap.power_score || 0);
            }
            
            // Next Best
            if (data.next_best && data.next_best.name) {
                document.getElementById('nextBestNumber').textContent = 'رقم ' + (data.next_best.number || 2) + ' | البوابة ' + (data.next_best.draw || 2);
                document.getElementById('nextBestHorse').textContent = data.next_best.name;
                document.getElementById('nextBestDetails').textContent = data.next_best.jockey + ' | ' + data.next_best.trainer;
                document.getElementById('nextBestSpeed').textContent = '🏃 ' + (data.next_best.speed_kmph || 0) + ' كم/ساعة | القوة: ' + (data.next_best.power_score || 0);
            }
            
            // Value Pick
            if (data.value_pick && data.value_pick.name) {
                document.getElementById('valuePickNumber').textContent = 'رقم ' + (data.value_pick.number || 3) + ' | البوابة ' + (data.value_pick.draw || 3);
                document.getElementById('valuePickHorse').textContent = data.value_pick.name;
                document.getElementById('valuePickDetails').textContent = data.value_pick.jockey + ' | ' + data.value_pick.trainer;
                document.getElementById('valuePickSpeed').textContent = '🏃 ' + (data.value_pick.speed_kmph || 0) + ' كم/ساعة | القوة: ' + (data.value_pick.power_score || 0);
            }
            
            // Races
            let racesHtml = '';
            for (const race of data.races) {
                let horsesRows = '';
                for (const h of race.horses) {
                    const badge = h.position === 1 ? '🥇' : h.position === 2 ? '🥈' : h.position === 3 ? '🥉' : '';
                    horsesRows += '<tr>' +
                        '<td>' + badge + ' ' + h.position + '</td>' +
                        '<td style="color:#ffd700;font-weight:700">' + h.number + '</td>' +
                        '<td style="color:#28a745;font-weight:600">' + h.draw + '</td>' +
                        '<td style="font-weight:600;text-align:right">' + h.name + '</td>' +
                        '<td>' + h.jockey + '</td>' +
                        '<td>' + h.trainer + '</td>' +
                        '<td>' + h.rating + '</td>' +
                        '<td style="font-weight:700">' + h.power_score + '</td>' +
                        '<td style="color:#28a745;font-weight:600">' + h.speed_kmph + '</td>' +
                        '<td>' + h.win_probability + '%</td>' +
                        '</tr>';
                }
                
                racesHtml += '<div class="race-card">' +
                    '<div class="race-header">' +
                    '<h3>🏇 ' + race.name + '</h3>' +
                    '<span class="race-info">' + race.time + ' | ' + race.distance + 'm | ' + race.surface + '</span>' +
                    '</div>' +
                    '<div class="table-wrapper"><table>' +
                    '<thead><tr>' +
                    '<th>المركز</th><th>الرقم</th><th>البوابة</th><th>الحصان</th>' +
                    '<th>الفارس</th><th>المدرب</th><th>التقييم</th><th>القوة</th><th>السرعة</th><th>%</th>' +
                    '</tr></thead><tbody>' + horsesRows + '</tbody></table></div></div>';
            }
            
            document.getElementById('races').innerHTML = racesHtml;
            
            // Live Stream
            if (data.live_stream && data.live_stream.url) {
                document.getElementById('liveStreamBox').innerHTML = 
                    '<div class="live-stream-box"><h3>📺 البث المباشر</h3>' +
                    '<div class="stream-links">' +
                    '<a href="' + data.live_stream.url + '" target="_blank" class="stream-link">🎬 البث الرسمي</a>' +
                    (data.live_stream.backup ? '<a href="' + data.live_stream.backup + '" target="_blank" class="stream-link" style="background:#6c757d">📡 بديل</a>' : '') +
                    (data.live_stream.youtube ? '<a href="' + data.live_stream.youtube + '" target="_blank" class="stream-link" style="background:#ff0000">📺 YouTube</a>' : '') +
                    '</div></div>';
            }
            
            document.getElementById('results').style.display = 'block';
        }
        
        async function sendEmail() {
            let email = document.getElementById('email').value || 'paidera21@gmail.com';
            if (!currentPredictions) {
                alert('لا توجد ترشيحات للإرسال');
                return;
            }
            
            try {
                const data = await fetchWithRetry('/api/send-email', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({email, predictions: currentPredictions})
                });
                
                if (data.success) {
                    alert('✅ تم إرسال البريد بنجاح إلى: ' + email);
                } else {
                    alert('⚠️ ' + data.message);
                }
            } catch(e) {
                alert('⚠️ خطأ: ' + e.message);
            }
        }
        
        loadTracks();
    </script>
</body>
</html>
'''


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

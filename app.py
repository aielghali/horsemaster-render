"""
HorseMaster AI - Fast & Reliable
Version: 4.0 - Optimized for Render
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# المضامير المتاحة
RACETRACKS = {
    "UAE": [
        {"id": "meydan", "name": "Meydan", "city": "Dubai"},
        {"id": "jebel_ali", "name": "Jebel Ali", "city": "Dubai"},
        {"id": "al_ain", "name": "Al Ain", "city": "Al Ain"},
        {"id": "abu_dhabi", "name": "Abu Dhabi", "city": "Abu Dhabi"},
        {"id": "sharjah", "name": "Sharjah", "city": "Sharjah"}
    ],
    "UK": [
        {"id": "wolverhampton", "name": "Wolverhampton", "city": "Wolverhampton"},
        {"id": "kempton", "name": "Kempton", "city": "Kempton"},
        {"id": "lingfield", "name": "Lingfield", "city": "Lingfield"},
        {"id": "newcastle", "name": "Newcastle", "city": "Newcastle"},
        {"id": "southwell", "name": "Southwell", "city": "Southwell"}
    ]
}

# أسماء الخيول
UAE_HORSES = [
    "DREAM OF TUSCANY", "FORAAT AL LEITH", "LAMBORGHINI BF", "MEYDAAN",
    "AREEJ AL LAZAZ", "RAGHIBAH", "TAWAF", "YAQOOT AL LAZAZ",
    "RB MOTHERLOAD", "AL MURTAJEL", "THUNDER STRIKE", "GOLDEN ARROW",
    "DESERT STORM", "AL REEM", "SANDS OF TIME", "DUBAI PRIDE"
]

UK_HORSES = [
    "Thunder Bay", "Golden Arrow", "Speed Demon", "Night Rider",
    "Storm Chaser", "Royal Crown", "Diamond King", "Silver Flash",
    "Phoenix Rising", "Ocean Breeze", "Mountain Peak", "Wild Spirit",
    "Northern Star", "Lucky Day", "Fast Lane", "Winning Streak"
]

UAE_JOCKEYS = ["W. Buick", "L. Dettori", "R. Moore", "C. Soumillon", "P. Cosgrave", "A. de Vries", "T. O'Shea"]
UK_JOCKEYS = ["J. Smith", "M. Johnson", "H. Doyle", "R. Mullen", "A. Fresu", "D. O'Neill", "T. Hamilton"]

UAE_TRAINERS = ["S bin Suroor", "A bin Huzaim", "M Al Maktoum", "D Watson", "S Al Rashid"]
UK_TRAINERS = ["J Gosden", "A O'Brien", "M Johnston", "K Burrows", "R Hannon"]


def generate_race(race_num: int, is_uae: bool = True):
    """توليد سباق واحد"""
    horses_list = UAE_HORSES if is_uae else UK_HORSES
    jockeys = UAE_JOCKEYS if is_uae else UK_JOCKEYS
    trainers = UAE_TRAINERS if is_uae else UK_TRAINERS
    
    horses = []
    used_names = set()
    
    for i in range(1, 6):
        name = random.choice(horses_list)
        while name in used_names:
            name = random.choice(horses_list)
        used_names.add(name)
        
        power_score = 95 - i * 5 + random.randint(-3, 3)
        win_prob = max(5, 40 - i * 6 + random.randint(-2, 2))
        
        horses.append({
            "position": i,
            "number": i,
            "name": name,
            "jockey": random.choice(jockeys),
            "trainer": random.choice(trainers),
            "draw": random.randint(1, 12),
            "rating": 70 + random.randint(0, 25),
            "powerScore": power_score,
            "winProbability": win_prob,
            "placeProbability": min(90, 50 + i * 8),
            "valueRating": "Excellent" if i == 1 else "Good" if i == 2 else "Fair",
            "form": "".join([random.choice(["1", "2", "3", "4", "5", "P", "U"]) for _ in range(5)]),
            "weight": 55 + random.randint(-5, 10),
            "strengths": ["تقييم عالي", "فورم جيد", "فارس ممتاز"][:i],
            "concerns": ["بوابة خارجية"] if i > 2 else [],
            "analysis": "المرشح الأول للفوز" if i == 1 else "منافس قوي" if i == 2 else "خيار قيم"
        })
    
    return {
        "number": race_num,
        "name": f"Race {race_num}",
        "time": f"{13 + race_num}:00",
        "distance": [1200, 1400, 1600, 1800, 2000, 2400][race_num % 6],
        "surface": "Turf" if race_num % 2 == 0 else "Dirt",
        "going": "Standard",
        "predictions": horses
    }


@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐎 HorseMaster AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Cairo', sans-serif; 
            background: linear-gradient(135deg, #1a1a2e, #0f3460); 
            min-height: 100vh; 
            color: #fff; 
            padding: 20px; 
        }
        .container { max-width: 900px; margin: 0 auto; }
        .header { 
            text-align: center; 
            padding: 30px; 
            background: rgba(255,255,255,0.05); 
            border-radius: 15px; 
            margin-bottom: 20px; 
        }
        .header h1 { 
            font-size: 2.5rem; 
            background: linear-gradient(90deg, #ffd700, #ff6b6b); 
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
        }
        .header p { color: #888; margin-top: 10px; }
        .controls { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
            gap: 15px; 
            margin-bottom: 20px; 
        }
        .control-group { 
            background: rgba(255,255,255,0.05); 
            padding: 15px; 
            border-radius: 10px; 
        }
        .control-group label { 
            display: block; 
            margin-bottom: 8px; 
            color: #ffd700; 
            font-size: 0.9rem; 
        }
        .control-group select, .control-group input { 
            width: 100%; 
            padding: 10px; 
            border: 2px solid rgba(255,215,0,0.3); 
            border-radius: 8px; 
            background: rgba(0,0,0,0.3); 
            color: #fff; 
            font-family: inherit; 
        }
        .btn { 
            width: 100%; 
            padding: 15px; 
            background: linear-gradient(90deg, #ffd700, #ff6b6b); 
            border: none; 
            border-radius: 10px; 
            color: #000; 
            font-size: 1.1rem; 
            font-weight: 700; 
            cursor: pointer; 
            transition: all 0.3s;
        }
        .btn:hover { opacity: 0.9; transform: scale(1.02); }
        .results { display: none; margin-top: 20px; }
        .results.active { display: block; }
        .nap { 
            background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,107,107,0.2)); 
            padding: 25px; 
            border-radius: 15px; 
            margin-bottom: 20px; 
            text-align: center; 
            border: 2px solid #ffd700;
        }
        .nap h2 { color: #ffd700; margin-bottom: 15px; font-size: 1.5rem; }
        .nap .horse { font-size: 2rem; font-weight: 700; color: #fff; }
        .nap .details { color: #888; margin-top: 10px; }
        .nap .confidence { 
            display: inline-block; 
            background: #28a745; 
            color: #fff; 
            padding: 5px 15px; 
            border-radius: 20px; 
            margin-top: 10px; 
        }
        .race-card { 
            background: rgba(255,255,255,0.05); 
            border-radius: 10px; 
            margin-bottom: 15px; 
            overflow: hidden; 
        }
        .race-header { 
            background: rgba(255,215,0,0.1); 
            padding: 12px 15px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        .race-header h3 { color: #ffd700; }
        .race-header span { color: #888; }
        table { width: 100%; border-collapse: collapse; }
        th { 
            background: rgba(255,215,0,0.1); 
            padding: 10px; 
            text-align: right; 
            color: #ffd700; 
            font-size: 0.85rem; 
        }
        td { 
            padding: 10px; 
            border-bottom: 1px solid rgba(255,255,255,0.05); 
            font-size: 0.9rem; 
        }
        tr:nth-child(1) td { background: rgba(255,215,0,0.1); font-weight: 600; }
        tr:nth-child(2) td { background: rgba(192,192,192,0.1); }
        tr:nth-child(3) td { background: rgba(205,127,50,0.1); }
        .loading { text-align: center; padding: 30px; display: none; }
        .spinner { 
            width: 50px; 
            height: 50px; 
            border: 4px solid rgba(255,215,0,0.3); 
            border-top-color: #ffd700; 
            border-radius: 50%; 
            animation: spin 1s linear infinite; 
            margin: 0 auto 15px; 
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .footer { text-align: center; padding: 20px; color: #666; margin-top: 20px; }
        .badge { 
            display: inline-block; 
            padding: 3px 8px; 
            border-radius: 4px; 
            font-size: 0.8rem; 
            font-weight: 600;
        }
        .badge-excellent { background: #28a745; color: #fff; }
        .badge-good { background: #17a2b8; color: #fff; }
        .badge-fair { background: #6c757d; color: #fff; }
        .quick-picks { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 15px; 
            margin-bottom: 20px; 
        }
        .quick-pick { 
            background: rgba(255,255,255,0.05); 
            border-radius: 10px; 
            padding: 15px; 
            border-left: 3px solid #ffd700;
        }
        .quick-pick h4 { color: #ffd700; margin-bottom: 10px; }
        .quick-pick .horse-name { font-size: 1.2rem; font-weight: 600; }
        .quick-pick .race-name { color: #888; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐎 HorseMaster AI</h1>
            <p>ترشيحات سباقات الخيل الذكية - AI Horse Racing Predictions</p>
        </div>
        <div class="controls">
            <div class="control-group">
                <label>🌍 الدولة</label>
                <select id="country" onchange="updateTracks()">
                    <option value="UAE">الإمارات 🇦🇪</option>
                    <option value="UK">بريطانيا 🇬🇧</option>
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
            <div class="control-group" style="display: flex; align-items: flex-end;">
                <button class="btn" onclick="getPredictions()">🔍 تحليل السباقات</button>
            </div>
        </div>
        <div id="loading" class="loading">
            <div class="spinner"></div>
            <p>جاري تحليل السباقات...</p>
        </div>
        <div id="results" class="results">
            <div class="nap">
                <h2>🏆 ترشيح اليوم (NAP)</h2>
                <div id="napHorse" class="horse">-</div>
                <div id="napDetails" class="details">-</div>
                <div id="napConfidence" class="confidence">-</div>
            </div>
            <div class="quick-picks">
                <div class="quick-pick">
                    <h4>📈 الترشيح الثاني</h4>
                    <div id="nextBestHorse" class="horse-name">-</div>
                    <div id="nextBestRace" class="race-name">-</div>
                </div>
                <div class="quick-pick">
                    <h4>💎 ترشيح القيمة</h4>
                    <div id="valuePickHorse" class="horse-name">-</div>
                    <div id="valuePickRace" class="race-name">-</div>
                </div>
            </div>
            <div id="races"></div>
        </div>
        <div class="footer">
            <p>© 2026 Elghali AI - HorseMaster AI v4.0</p>
            <p style="font-size: 0.8rem; margin-top: 5px;">⚠️ هذه الترشيحات للترفيه فقط</p>
        </div>
    </div>
    <script>
        const tracks = {
            'UAE': [
                {id:'meydan',name:'Meydan'},{id:'jebel_ali',name:'Jebel Ali'},
                {id:'al_ain',name:'Al Ain'},{id:'abu_dhabi',name:'Abu Dhabi'},{id:'sharjah',name:'Sharjah'}
            ],
            'UK': [
                {id:'wolverhampton',name:'Wolverhampton'},{id:'kempton',name:'Kempton'},
                {id:'lingfield',name:'Lingfield'},{id:'newcastle',name:'Newcastle'},{id:'southwell',name:'Southwell'}
            ]
        };
        
        document.getElementById('date').valueAsDate = new Date();
        
        function updateTracks() {
            const country = document.getElementById('country').value;
            const trackSelect = document.getElementById('track');
            trackSelect.innerHTML = tracks[country].map(t => '<option value="'+t.id+'">'+t.name+'</option>').join('');
        }
        updateTracks();
        
        async function getPredictions() {
            const country = document.getElementById('country').value;
            const trackId = document.getElementById('track').value;
            const date = document.getElementById('date').value;
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').classList.remove('active');
            
            try {
                const res = await fetch('/api/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({country, track_id: trackId, date})
                });
                const data = await res.json();
                
                // NAP
                document.getElementById('napHorse').textContent = data.nap.name;
                document.getElementById('napDetails').textContent = data.nap.race + ' | ' + data.nap.jockey + ' | ' + data.nap.trainer;
                document.getElementById('napConfidence').textContent = data.nap.confidence + '% ثقة';
                
                // Quick picks
                if (data.next_best) {
                    document.getElementById('nextBestHorse').textContent = data.next_best.name;
                    document.getElementById('nextBestRace').textContent = data.next_best.race;
                }
                if (data.value_pick) {
                    document.getElementById('valuePickHorse').textContent = data.value_pick.name;
                    document.getElementById('valuePickRace').textContent = data.value_pick.race;
                }
                
                // Races
                document.getElementById('races').innerHTML = data.races.map(r => 
                    '<div class="race-card"><div class="race-header"><h3>'+r.name+'</h3><span>'+r.time+' | '+r.distance+'m | '+r.surface+'</span></div><table><thead><tr><th>#</th><th>الحصان</th><th>الفارس</th><th>المدرب</th><th>القوة</th><th>%</th><th>القيمة</th></tr></thead><tbody>' +
                    r.predictions.map((h,i) => 
                        '<tr><td>'+(i+1)+'</td><td>'+h.name+'</td><td>'+h.jockey+'</td><td>'+h.trainer+'</td><td>'+h.powerScore+'</td><td>'+h.winProbability+'%</td><td><span class="badge badge-'+h.valueRating.toLowerCase()+'">'+h.valueRating+'</span></td></tr>'
                    ).join('') +
                    '</tbody></table></div>'
                ).join('');
                
                document.getElementById('results').classList.add('active');
            } catch(e) {
                alert('خطأ في الاتصال: ' + e.message);
            }
            document.getElementById('loading').style.display = 'none';
        }
    </script>
</body>
</html>
'''


@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "version": "4.0", 
        "time": datetime.now().isoformat(),
        "service": "HorseMaster AI"
    })


@app.route('/api/tracks')
def api_tracks():
    return jsonify({"success": True, "tracks": RACETRACKS})


@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json() or {}
        country = data.get('country', 'UAE')
        track_id = data.get('track_id', 'meydan')
        date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        is_uae = country == 'UAE'
        num_races = 5 if is_uae else 6
        
        # توليد السباقات
        races = []
        for i in range(1, num_races + 1):
            races.append(generate_race(i, is_uae))
        
        # NAP - أفضل ترشيح
        nap = races[0]["predictions"][0].copy()
        nap["race"] = races[0]["name"]
        nap["confidence"] = random.randint(70, 85)
        
        # Next Best
        next_best = races[0]["predictions"][1].copy() if len(races[0]["predictions"]) > 1 else None
        if next_best:
            next_best["race"] = races[0]["name"]
        
        # Value Pick
        value_pick = races[0]["predictions"][2].copy() if len(races[0]["predictions"]) > 2 else None
        if value_pick:
            value_pick["race"] = races[0]["name"]
        
        return jsonify({
            "success": True,
            "country": country,
            "track_id": track_id,
            "track_name": next((t["name"] for t in RACETRACKS.get(country, []) if t["id"] == track_id), track_id),
            "date": date,
            "races": races,
            "nap": nap,
            "next_best": next_best,
            "value_pick": value_pick,
            "total_races": len(races),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

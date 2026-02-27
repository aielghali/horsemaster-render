#!/usr/bin/env python3
"""
HorseMaster AI - Local Data Scraper
====================================
يجمع البيانات الحقيقية من المصادر ويرسلها للتطبيق

التشغيل:
    python race_bot.py --track meydan --date 2026-02-27
    
الإرسال للسيرفر:
    python race_bot.py --track meydan --date 2026-02-27 --upload
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime
import argparse
import os

# Headers for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

# Source URLs
SOURCES = {
    'emirates_racing': {
        'racecards': 'https://www.emiratesracing.com/racecards',
        'results': 'https://www.emiratesracing.com/results/{date}',
    },
    'racing_post': {
        'racecards': 'https://www.racingpost.com/racecards/',
        'results': 'https://www.racingpost.com/results/{track}/{date}',
    },
    'timeform': {
        'racecards': 'https://www.timeform.com/horse-racing/racecards/',
    },
    'sky_racing': {
        'racecards': 'https://www.skyracingworld.com/racecards',
        'results': 'https://www.skyracingworld.com/results',
    },
    'sporting_life': {
        'racecards': 'https://www.sportinglife.com/racing/racecards',
    },
    'at_the_races': {
        'racecards': 'https://www.attheraces.com/racecards',
    },
    'dubai_racing': {
        'racecards': 'https://www.dubairacing.org/racecards',
    }
}

# Track mappings
TRACK_URLS = {
    'meydan': {
        'emirates': 'meydan',
        'racingpost': 'united-arab-emirates/meydan',
        'timeform': 'united-arab-emirates/meydan',
    },
    'jebel_ali': {
        'emirates': 'jebel-ali',
        'racingpost': 'jebel-ali',
        'timeform': 'united-arab-emirates/jebel-ali',
    },
    'al_ain': {
        'emirates': 'al-ain',
        'racingpost': 'al-ain',
        'timeform': 'united-arab-emirates/al-ain',
    },
    'abu_dhabi': {
        'emirates': 'abu-dhabi',
        'racingpost': 'abu-dhabi',
        'timeform': 'united-arab-emirates/abu-dhabi',
    },
    'sharjah': {
        'emirates': 'sharjah',
        'racingpost': 'sharjah',
        'timeform': 'united-arab-emirates/sharjah',
    },
    'wolverhampton': {
        'racingpost': 'wolverhampton',
        'timeform': 'gb/wolverhampton',
        'sportinglife': 'wolverhampton',
    },
    'kempton': {
        'racingpost': 'kempton',
        'timeform': 'gb/kempton',
    },
    'lingfield': {
        'racingpost': 'lingfield',
        'timeform': 'gb/lingfield',
    },
    'newcastle': {
        'racingpost': 'newcastle',
        'timeform': 'gb/newcastle',
    },
    'southwell': {
        'racingpost': 'southwell',
        'timeform': 'gb/southwell',
    }
}


class RaceBot:
    def __init__(self, track: str, date: str = None):
        self.track = track.lower().replace(' ', '_')
        self.date = date or datetime.now().strftime('%Y-%m-%d')
        self.races = []
        self.horses_data = {}
        
    def fetch_from_emirates_racing(self):
        """جلب البيانات من Emirates Racing"""
        print(f"📡 Fetching from Emirates Racing...")
        
        try:
            url = f"https://www.emiratesracing.com/racecards/{self.date}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # البحث عن بطاقات السباقات
                race_cards = soup.find_all('div', class_='race-card')
                
                for card in race_cards:
                    race_data = self._parse_race_card(card)
                    if race_data:
                        self.races.append(race_data)
                        
                print(f"   ✅ Found {len(self.races)} races")
                return True
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        return False
    
    def fetch_from_racing_post(self):
        """جلب البيانات من Racing Post"""
        print(f"📡 Fetching from Racing Post...")
        
        track_info = TRACK_URLS.get(self.track, {})
        rp_path = track_info.get('racingpost', self.track)
        
        try:
            url = f"https://www.racingpost.com/racecards/{rp_path}/{self.date}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # استخراج البيانات
                horses = self._parse_racing_post(soup)
                if horses:
                    print(f"   ✅ Found {len(horses)} horses")
                    self.horses_data['racingpost'] = horses
                    return True
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        return False
    
    def fetch_from_timeform(self):
        """جلب البيانات من Timeform"""
        print(f"📡 Fetching from Timeform...")
        
        track_info = TRACK_URLS.get(self.track, {})
        tf_path = track_info.get('timeform', self.track)
        
        try:
            url = f"https://www.timeform.com/horse-racing/racecards/{tf_path}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                horses = self._parse_timeform(soup)
                if horses:
                    print(f"   ✅ Found {len(horses)} horses")
                    self.horses_data['timeform'] = horses
                    return True
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        return False
    
    def fetch_from_sky_racing(self):
        """جلب البيانات من Sky Racing World (أستراليا)"""
        print(f"📡 Fetching from Sky Racing World...")
        
        try:
            url = "https://www.skyracingworld.com/racecards"
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                horses = self._parse_sky_racing(soup)
                if horses:
                    print(f"   ✅ Found {len(horses)} horses")
                    self.horses_data['skyracing'] = horses
                    return True
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        return False
    
    def _parse_race_card(self, card) -> dict:
        """تحليل بطاقة السباق"""
        try:
            race_num = card.find('span', class_='race-number')
            race_num = race_num.text if race_num else '1'
            
            time_elem = card.find('span', class_='race-time')
            race_time = time_elem.text if time_elem else ''
            
            distance_elem = card.find('span', class_='distance')
            distance = distance_elem.text if distance_elem else ''
            
            horses = []
            horse_rows = card.find_all('tr', class_='horse-row')
            
            for row in horse_rows:
                horse = self._parse_horse_row(row)
                if horse:
                    horses.append(horse)
            
            return {
                'number': int(re.search(r'\d+', race_num).group()) if race_num else 1,
                'time': race_time,
                'distance': distance,
                'horses': horses
            }
            
        except Exception as e:
            return None
    
    def _parse_horse_row(self, row) -> dict:
        """تحليل صف الحصان"""
        try:
            number = row.find('td', class_='horse-number')
            name = row.find('td', class_='horse-name')
            jockey = row.find('td', class_='jockey')
            trainer = row.find('td', class_='trainer')
            weight = row.find('td', class_='weight')
            draw = row.find('td', class_='draw')
            
            return {
                'number': int(number.text.strip()) if number else 0,
                'name': name.text.strip() if name else '',
                'jockey': jockey.text.strip() if jockey else '',
                'trainer': trainer.text.strip() if trainer else '',
                'weight': weight.text.strip() if weight else '',
                'draw': int(draw.text.strip()) if draw else 0,
            }
            
        except:
            return None
    
    def _parse_racing_post(self, soup) -> list:
        """تحليل Racing Post"""
        horses = []
        
        # البحث عن عناصر الخيول
        horse_elements = soup.find_all(['tr', 'div'], class_=lambda x: x and 'horse' in str(x).lower())
        
        for elem in horse_elements:
            try:
                text = elem.get_text()
                
                # استخراج رقم الحصان
                num_match = re.search(r'^\s*(\d{1,2})', text)
                number = int(num_match.group(1)) if num_match else 0
                
                # استخراج الاسم (يكون عادة بحروف كبيرة)
                name_match = re.search(r'[A-Z][A-Z\s]+[A-Z]', text)
                name = name_match.group().strip() if name_match else ''
                
                if name:
                    horses.append({
                        'number': number,
                        'name': name,
                        'source': 'racingpost'
                    })
                    
            except:
                continue
        
        return horses
    
    def _parse_timeform(self, soup) -> list:
        """تحليل Timeform"""
        horses = []
        
        # Timeform يستخدم بنية مختلفة
        race_sections = soup.find_all('div', class_='w-racecard-runner')
        
        for section in race_sections:
            try:
                number = section.find('span', class_='w-racecard-runner__saddle-cloth')
                name = section.find('a', class_='w-racecard-runner__horse-name')
                
                if name:
                    horses.append({
                        'number': int(number.text) if number else 0,
                        'name': name.text.strip(),
                        'source': 'timeform'
                    })
                    
            except:
                continue
        
        return horses
    
    def _parse_sky_racing(self, soup) -> list:
        """تحليل Sky Racing"""
        horses = []
        
        # البحث عن العناصر
        runners = soup.find_all(['tr', 'div'], class_=lambda x: x and 'runner' in str(x).lower())
        
        for runner in runners:
            try:
                text = runner.get_text()
                
                # استخراج البيانات
                num_match = re.search(r'(\d{1,2})\.', text)
                name_match = re.search(r'\d\.\s+([A-Za-z\s]+)', text)
                
                if name_match:
                    horses.append({
                        'number': int(num_match.group(1)) if num_match else 0,
                        'name': name_match.group(1).strip(),
                        'source': 'skyracing'
                    })
                    
            except:
                continue
        
        return horses
    
    def fetch_all(self):
        """جلب البيانات من جميع المصادر"""
        print(f"\n{'='*50}")
        print(f"🐎 HorseMaster AI - Data Fetcher")
        print(f"📍 Track: {self.track.upper()}")
        print(f"📅 Date: {self.date}")
        print(f"{'='*50}\n")
        
        # UAE tracks
        if self.track in ['meydan', 'jebel_ali', 'al_ain', 'abu_dhabi', 'sharjah']:
            self.fetch_from_emirates_racing()
            self.fetch_from_racing_post()
            self.fetch_from_timeform()
            self.fetch_from_dubai_racing()
        
        # UK tracks
        elif self.track in ['wolverhampton', 'kempton', 'lingfield', 'newcastle', 'southwell']:
            self.fetch_from_racing_post()
            self.fetch_from_timeform()
            self.fetch_from_sporting_life()
        
        # Australia
        elif self.track in ['randwick', 'flemington', 'rosehill', 'caulfield']:
            self.fetch_from_sky_racing()
        
        else:
            # Generic fetch
            self.fetch_from_racing_post()
            self.fetch_from_timeform()
        
        return self.merge_data()
    
    def fetch_from_dubai_racing(self):
        """جلب من Dubai Racing"""
        print(f"📡 Fetching from Dubai Racing...")
        
        try:
            url = "https://www.dubairacing.org/racecards"
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                horses = self._parse_dubai_racing(soup)
                if horses:
                    print(f"   ✅ Found {len(horses)} horses")
                    self.horses_data['dubairacing'] = horses
                    return True
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        return False
    
    def fetch_from_sporting_life(self):
        """جلب من Sporting Life"""
        print(f"📡 Fetching from Sporting Life...")
        
        try:
            url = f"https://www.sportinglife.com/racing/racecards/{self.track}/{self.date}"
            response = requests.get(url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                horses = self._parse_sporting_life(soup)
                if horses:
                    print(f"   ✅ Found {len(horses)} horses")
                    self.horses_data['sportinglife'] = horses
                    return True
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        return False
    
    def _parse_dubai_racing(self, soup) -> list:
        """تحليل Dubai Racing"""
        horses = []
        
        runners = soup.find_all(['tr', 'div'], class_=lambda x: x and 'runner' in str(x).lower())
        
        for runner in runners:
            try:
                text = runner.get_text()
                name_match = re.search(r'[A-Z][A-Z\s]+', text)
                
                if name_match:
                    horses.append({
                        'name': name_match.group().strip(),
                        'source': 'dubairacing'
                    })
            except:
                continue
        
        return horses
    
    def _parse_sporting_life(self, soup) -> list:
        """تحليل Sporting Life"""
        horses = []
        
        runners = soup.find_all(['tr', 'li'], class_=lambda x: x and 'runner' in str(x).lower())
        
        for runner in runners:
            try:
                text = runner.get_text()
                name_match = re.search(r'\d+\s+([A-Za-z][A-Za-z\s]+)', text)
                
                if name_match:
                    horses.append({
                        'name': name_match.group(1).strip(),
                        'source': 'sportinglife'
                    })
            except:
                continue
        
        return horses
    
    def merge_data(self) -> dict:
        """دمج البيانات من جميع المصادر"""
        all_horses = []
        
        # جمع كل الخيول
        for source, horses in self.horses_data.items():
            for horse in horses:
                all_horses.append(horse)
        
        # إزالة المكررات
        unique_horses = {}
        for horse in all_horses:
            name = horse['name'].upper()
            if name not in unique_horses:
                unique_horses[name] = horse
            else:
                # دمج البيانات
                existing = unique_horses[name]
                if not existing.get('jockey') and horse.get('jockey'):
                    existing['jockey'] = horse['jockey']
                if not existing.get('trainer') and horse.get('trainer'):
                    existing['trainer'] = horse['trainer']
        
        result = {
            'track': self.track,
            'date': self.date,
            'fetched_at': datetime.now().isoformat(),
            'total_horses': len(unique_horses),
            'sources': list(self.horses_data.keys()),
            'horses': list(unique_horses.values())
        }
        
        print(f"\n{'='*50}")
        print(f"📊 النتائج:")
        print(f"   🐴 عدد الخيول: {result['total_horses']}")
        print(f"   📡 المصادر: {', '.join(result['sources'])}")
        print(f"{'='*50}\n")
        
        return result
    
    def save_to_file(self, filename: str = None):
        """حفظ البيانات في ملف"""
        if not filename:
            filename = f"racecard_{self.track}_{self.date}.json"
        
        data = self.merge_data()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 تم حفظ البيانات في: {filename}")
        return filename
    
    def upload_to_server(self, server_url: str = "https://horsemaster-render.onrender.com"):
        """رفع البيانات للسيرفر"""
        data = self.merge_data()
        
        try:
            response = requests.post(
                f"{server_url}/api/import-data",
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ تم رفع البيانات للسيرفر بنجاح!")
                return True
            else:
                print(f"❌ فشل الرفع: {response.status_code}")
                
        except Exception as e:
            print(f"❌ خطأ في الرفع: {e}")
        
        return False


def main():
    parser = argparse.ArgumentParser(description='HorseMaster AI Data Scraper')
    parser.add_argument('--track', '-t', required=True, help='Track name (e.g., meydan, wolverhampton)')
    parser.add_argument('--date', '-d', default=None, help='Date (YYYY-MM-DD)')
    parser.add_argument('--upload', '-u', action='store_true', help='Upload to server')
    parser.add_argument('--output', '-o', default=None, help='Output filename')
    
    args = parser.parse_args()
    
    bot = RaceBot(args.track, args.date)
    bot.fetch_all()
    
    filename = bot.save_to_file(args.output)
    
    if args.upload:
        bot.upload_to_server()
    
    print(f"\n✨ Done! Data saved to {filename}")


if __name__ == '__main__':
    main()

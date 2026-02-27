import ZAI from 'z-ai-web-dev-sdk';
import * as fs from 'fs';

const raceData = {
  "meeting": {
    "date": "27 February 2026",
    "venue": "Abu Dhabi Turf Club",
    "country": "UAE",
    "surface": "Turf",
    "going": "Good"
  },
  "races": [
    {
      "race_number": 1,
      "race_name": "Wathba Stallions Cup",
      "distance": "1400m",
      "time": "16:00",
      "class": "Purebred Arabian Stakes (4YO+)",
      "prize": "AED 66,000",
      "horses": [
        {"number": 1, "draw": 1, "name": "AF AL SANAA", "jockey": "A A Balushi", "trainer": "Hamza Al Hamida", "rating": 57},
        {"number": 2, "draw": 2, "name": "AF MAKEEN", "jockey": "Allaia Tiar", "trainer": "K Al Neyadi", "rating": 62},
        {"number": 3, "draw": 3, "name": "ALJAMRI", "jockey": "Silvestre De Sousa", "trainer": "Sir Bani Yas", "rating": 85},
        {"number": 4, "draw": 4, "name": "AF NAFITH", "jockey": "Mohamed Salym", "trainer": "Ernst Oertel", "rating": 80},
        {"number": 5, "draw": 5, "name": "AF GHAYYAR", "jockey": "Tadhg O'Shea", "trainer": "Ernst Oertel", "rating": 85},
        {"number": 6, "draw": 6, "name": "KOYAN DE CARRERE", "jockey": "Mohamed Salym", "trainer": "Nieshan", "rating": 64}
      ]
    },
    {
      "race_number": 2,
      "race_name": "The Crescent Light Stakes",
      "distance": "1600m",
      "time": "16:30",
      "class": "Listed Stakes",
      "prize": "AED 85,000",
      "horses": [
        {"number": 1, "draw": 1, "name": "AJRAD ATHBAH", "jockey": "Silvestre De Sousa", "trainer": "Majed Al Jahoori", "rating": 116},
        {"number": 2, "draw": 2, "name": "BUCANERO", "jockey": "Abdul Aziz Al Balushi", "trainer": "M Al Maktoum", "rating": 95},
        {"number": 3, "draw": 3, "name": "BAHWAN", "jockey": "Connor Beasley", "trainer": "M Shamsi", "rating": 125},
        {"number": 4, "draw": 4, "name": "KANTI DE BOZOULS", "jockey": "Sandro Paiva", "trainer": "France", "rating": 90},
        {"number": 5, "draw": 5, "name": "RB YAS SIR", "jockey": "Alexandre De Silva", "trainer": "Al Qasimi", "rating": 88},
        {"number": 6, "draw": 6, "name": "QUEPOS", "jockey": "Richard Mullen", "trainer": "Satish Seemar", "rating": 98}
      ]
    },
    {
      "race_number": 3,
      "race_name": "Soil of the Union",
      "distance": "1800m",
      "time": "17:00",
      "class": "Purebred Arabian Handicap (0-95)",
      "prize": "AED 75,000",
      "horses": [
        {"number": 1, "draw": 1, "name": "MN HATTAN", "jockey": "Abdul Aziz Al Balushi", "trainer": "M Al Maktoum", "rating": 75},
        {"number": 2, "draw": 2, "name": "INVICTUS AL ASHAI", "jockey": "Sandro Paiva", "trainer": "Ernst Oertel", "rating": 85},
        {"number": 3, "draw": 3, "name": "HAITHAM DE MIREVAL", "jockey": "Connor Beasley", "trainer": "M Shamsi", "rating": 78},
        {"number": 4, "draw": 4, "name": "AF TUBHER", "jockey": "Tadhg O'Shea", "trainer": "Ernst Oertel", "rating": 82},
        {"number": 5, "draw": 5, "name": "FIFRE AL MAURY", "jockey": "Richard Mullen", "trainer": "Satish Seemar", "rating": 80}
      ]
    },
    {
      "race_number": 4,
      "race_name": "Masar Almajd Mile",
      "distance": "1600m",
      "time": "17:30",
      "class": "Purebred Arabian Handicap (0-80)",
      "prize": "AED 66,000",
      "horses": [
        {"number": 1, "draw": 1, "name": "AF MARMUQ", "jockey": "Anderson Paiva", "trainer": "Ernst Oertel", "rating": 78},
        {"number": 2, "draw": 2, "name": "AF MUHEM", "jockey": "Tadhg O'Shea", "trainer": "Ernst Oertel", "rating": 75},
        {"number": 3, "draw": 3, "name": "AF SAQARA", "jockey": "Connor Beasley", "trainer": "M Al Maktoum", "rating": 72},
        {"number": 4, "draw": 4, "name": "ALGRAIN", "jockey": "Silvestre De Sousa", "trainer": "Majed Al Jahoori", "rating": 70},
        {"number": 5, "draw": 5, "name": "GOLDAMAL", "jockey": "Richard Mullen", "trainer": "Satish Seemar", "rating": 68}
      ]
    },
    {
      "race_number": 5,
      "race_name": "Darb Al Reeh Sprint",
      "distance": "1200m",
      "time": "18:00",
      "class": "Purebred Arabian Handicap (0-95)",
      "prize": "AED 66,000",
      "horses": [
        {"number": 1, "draw": 1, "name": "AF ALZAHI", "jockey": "Tadhg O'Shea", "trainer": "Ernst Oertel", "rating": 93},
        {"number": 2, "draw": 2, "name": "AF ALFAHEM", "jockey": "Connor Beasley", "trainer": "Ernst Oertel", "rating": 88},
        {"number": 3, "draw": 3, "name": "BA'ADI", "jockey": "Silvestre De Sousa", "trainer": "Majed Al Jahoori", "rating": 85},
        {"number": 4, "draw": 4, "name": "BARJAH", "jockey": "Richard Mullen", "trainer": "Satish Seemar", "rating": 82},
        {"number": 5, "draw": 5, "name": "AL HADAB", "jockey": "Sandro Paiva", "trainer": "M Shamsi", "rating": 80}
      ]
    },
    {
      "race_number": 6,
      "race_name": "The Flash of Sand Handicap",
      "distance": "1400m",
      "time": "19:00",
      "class": "Thoroughbred Handicap (0-70)",
      "prize": "AED 66,000",
      "horses": [
        {"number": 1, "draw": 1, "name": "ACACUS", "jockey": "Connor Beasley", "trainer": "Satish Seemar", "rating": 70},
        {"number": 2, "draw": 2, "name": "SILENT SPEECH", "jockey": "Qais Al Busaidi", "trainer": "Ibrahim Al Hadhrami", "rating": 68},
        {"number": 3, "draw": 3, "name": "HOPEFULLY YES", "jockey": "J Santiago", "trainer": "D Watson", "rating": 65},
        {"number": 4, "draw": 4, "name": "CHOSEN MARK", "jockey": "Richard Mullen", "trainer": "Satish Seemar", "rating": 62},
        {"number": 5, "draw": 5, "name": "HOT PROPERTY", "jockey": "Tadhg O'Shea", "trainer": "D Watson", "rating": 60}
      ]
    },
    {
      "race_number": 7,
      "race_name": "The Majlis Mile",
      "distance": "1600m",
      "time": "19:30",
      "class": "Thoroughbred Maiden Stakes",
      "prize": "AED 66,000",
      "horses": [
        {"number": 1, "draw": 1, "name": "BLACK FORGE", "jockey": "Tadhg O'Shea", "trainer": "D Watson", "rating": 0},
        {"number": 2, "draw": 2, "name": "BUCANERO", "jockey": "Connor Beasley", "trainer": "Satish Seemar", "rating": 0},
        {"number": 3, "draw": 3, "name": "ALMUZN", "jockey": "Silvestre De Sousa", "trainer": "Majed Al Jahoori", "rating": 0},
        {"number": 4, "draw": 4, "name": "DUKEDOM", "jockey": "Richard Mullen", "trainer": "Satish Seemar", "rating": 0},
        {"number": 5, "draw": 5, "name": "ELA MATA", "jockey": "Sandro Paiva", "trainer": "M Shamsi", "rating": 0},
        {"number": 6, "draw": 6, "name": "ALJAMRI", "jockey": "Abdul Aziz Al Balushi", "trainer": "M Al Maktoum", "rating": 0}
      ]
    }
  ]
};

async function main() {
  const zai = await ZAI.create();
  
  // Generate predictions for each race
  const predictions: any[] = [];
  
  for (const race of raceData.races) {
    const prompt = `Analyze this horse race and provide predictions.

Race ${race.race_number}: ${race.race_name}
Distance: ${race.distance}
Class: ${race.class}
Going: Good Turf

Horses:
${race.horses.map((h: any) => `${h.number}. ${h.name} (Draw ${h.draw}) - Jockey: ${h.jockey}, Trainer: ${h.trainer}, Rating: ${h.rating || 'Maiden'}`).join('\n')}

Provide:
1. NAP (Best bet) - Horse name and brief reason (2 sentences)
2. Next Best - Horse name and brief reason (2 sentences)  
3. Each Way Value - Horse name and brief reason (2 sentences)
4. Top 3 finish predictions

Consider: Rating, trainer form, jockey ability, draw advantage, distance suitability.

Return JSON format:
{
  "nap": {"horse": "NAME", "reason": "reason"},
  "next_best": {"horse": "NAME", "reason": "reason"},
  "each_way": {"horse": "NAME", "reason": "reason"},
  "top_3": ["1st", "2nd", "3rd"],
  "analysis": "Brief race analysis"
}`;

    const completion = await zai.chat.completions.create({
      messages: [{ role: 'user', content: prompt }]
    });
    
    const response = completion.choices[0]?.message?.content || '';
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    
    if (jsonMatch) {
      try {
        predictions.push({
          race: race.race_number,
          name: race.race_name,
          distance: race.distance,
          time: race.time,
          prediction: JSON.parse(jsonMatch[0])
        });
      } catch(e) {
        console.log(`Parse error for race ${race.race_number}`);
      }
    }
  }
  
  // Save predictions
  fs.writeFileSync('/home/z/my-project/download/abu_dhabi_predictions.json', JSON.stringify({ meeting: raceData.meeting, predictions }, null, 2));
  console.log('Predictions saved!');
  console.log(JSON.stringify(predictions, null, 2));
}

main().catch(console.error);

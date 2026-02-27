import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  const zai = await ZAI.create();
  
  // Multiple targeted searches
  const searches = [
    'Abu Dhabi 27 February 2026 Race 1 Wathba Stallions Cup AF GHAYYAR AF MAKEEN horses list',
    'Abu Dhabi 27 February 2026 Race 2 Crescent Light Stakes AJRAD ATHBAH BAHWAN horses',
    'Abu Dhabi 27 February 2026 Race 3 Soil of Union MN HATTAN INVICTUS horses',
    'Abu Dhabi 27 February 2026 Race 4 Masar Almajd Mile horses entries',
    'Abu Dhabi 27 February 2026 Race 5 Darb Al Reeh Sprint AF MARMUQ horses',
    'Abu Dhabi 27 February 2026 Race 6 Flash of Sand Handicap SILENT SPEECH horses',
    'Abu Dhabi 27 February 2026 Race 7 Majlis Mile BLACK FORGE ALJAMRI horses'
  ];
  
  let allData = '';
  
  for (const query of searches) {
    const results = await zai.functions.invoke('web_search', { query, num: 5 });
    allData += '\n' + results.map((r: any) => r.snippet).join('\n');
  }
  
  // Now use LLM to create comprehensive race card
  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'system',
        content: `You are a horse racing expert. Create a complete race card for Abu Dhabi on 27 February 2026.

Based on the search snippets, extract ALL horses for each race (7 races total).

Return ONLY valid JSON with this exact structure:
{
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
      "class": "Purebred Arabian Stakes",
      "prize_money": "AED 66,000",
      "horses": [
        {"number": 1, "draw": 1, "name": "Horse Name", "jockey": "Jockey", "trainer": "Trainer", "rating": 85}
      ]
    }
  ]
}

Include ALL horses you can identify. Be comprehensive.`
      },
      {
        role: 'user',
        content: `Create complete race card from these search results:\n\n${allData}`
      }
    ]
  });
  
  const responseText = completion.choices[0]?.message?.content || '';
  // Extract JSON from response
  const jsonMatch = responseText.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    console.log(jsonMatch[0]);
  } else {
    console.log(responseText);
  }
}

main().catch(console.error);

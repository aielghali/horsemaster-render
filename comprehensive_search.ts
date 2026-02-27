import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  const zai = await ZAI.create();
  
  // Very specific searches
  const searches = [
    '"Abu Dhabi" "27 February 2026" racecard horses jockeys trainers',
    'emiratesracing 27 Feb 2026 Abu Dhabi declarations all horses',
    '"Abu Dhabi Turf Club" 27/02/2026 race meeting horses list',
    'ERA Abu Dhabi February 27 2026 race 1 2 3 4 5 6 7 horses',
    'Abu Dhabi horse racing 27-02-2026 full card runners'
  ];
  
  let allSnippets = '';
  
  for (const query of searches) {
    const results = await zai.functions.invoke('web_search', { query, num: 10 });
    allSnippets += '\n' + results.map((r: any) => `${r.name}\n${r.snippet}`).join('\n---\n');
  }
  
  // Use LLM to create comprehensive data
  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'system',
        content: `You are a horse racing expert specializing in UAE racing.

Create a COMPLETE race card for Abu Dhabi Turf Club on 27 February 2026.

IMPORTANT: Based on the search data, there are 7 races. Include ALL horses you can identify.

For each horse provide:
- number: saddlecloth number (1-14)
- draw: starting stall position  
- name: horse name in CAPS
- jockey: jockey name
- trainer: trainer name
- rating: official rating (if known)
- weight: weight in kgs (if known)

For thoroughbred horses (races 6-7), use Thoroughbred naming.
For Purebred Arabian horses (races 1-5), names often start with AF, RB, or Arabic names.

Return ONLY valid JSON:
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
      "class": "Purebred Arabian Stakes (4YO+)",
      "prize": "AED 66,000",
      "horses": [
        {"number": 1, "draw": 1, "name": "HORSE NAME", "jockey": "Jockey", "trainer": "Trainer", "rating": 85, "weight": 56}
      ]
    }
  ]
}`
      },
      {
        role: 'user',
        content: `Create the complete race card from these search results:\n\n${allSnippets}`
      }
    ]
  });
  
  const response = completion.choices[0]?.message?.content || '';
  // Extract JSON
  const jsonMatch = response.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    console.log(jsonMatch[0]);
  } else {
    console.log(response);
  }
}

main().catch(console.error);

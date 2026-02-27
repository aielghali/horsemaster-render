import ZAI from 'z-ai-web-dev-sdk';
import * as fs from 'fs';

async function main() {
  const zai = await ZAI.create();
  
  // Read all races from the main page
  const result = await zai.functions.invoke('page_reader', {
    url: 'https://emiratesracing.com/racecard/2026-02-27/all/declarations'
  });
  
  const html = result.data?.html || '';
  
  // Extract all table rows
  const rowMatches = html.match(/<tr[^>]*>[\s\S]*?<\/tr>/gi) || [];
  
  // Use LLM to parse and structure all the data
  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'system',
        content: `You are a horse racing data parser. Extract ALL horses from the provided raw HTML table data.

For each horse, extract:
- number: saddlecloth number
- draw: starting stall/position  
- name: horse name (in CAPS)
- jockey: jockey name
- trainer: trainer name
- rating: official rating number
- weight: weight in kg
- note: any notes like "NR" for non-runners

The data is from Abu Dhabi Turf Club on 27 February 2026. There are 7 races.

Return ONLY valid JSON:
{
  "races": [
    {
      "race_number": 1,
      "race_name": "Race name from data",
      "distance": "distance if found",
      "horses": [
        {"number": 1, "draw": 1, "name": "HORSE NAME", "jockey": "Jockey Name", "trainer": "Trainer Name", "rating": 85, "weight": 57, "note": ""}
      ]
    }
  ]
}

Extract EVERY single horse. Be thorough and accurate.`
      },
      {
        role: 'user',
        content: `Parse this raw horse racing data:\n\n${rowMatches.map(r => r.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()).join('\n')}`
      }
    ]
  });
  
  const response = completion.choices[0]?.message?.content || '';
  const jsonMatch = response.match(/\{[\s\S]*\}/);
  
  if (jsonMatch) {
    const data = JSON.parse(jsonMatch[0]);
    
    // Save to file
    fs.writeFileSync('/home/z/my-project/download/abu_dhabi_real_data.json', JSON.stringify(data, null, 2));
    
    console.log('=== EXTRACTED REAL DATA ===\n');
    console.log(JSON.stringify(data, null, 2));
    
    // Summary
    console.log('\n=== SUMMARY ===');
    let totalHorses = 0;
    for (const race of data.races) {
      console.log(`Race ${race.race_number}: ${race.horses.length} horses`);
      totalHorses += race.horses.length;
    }
    console.log(`Total: ${totalHorses} horses across ${data.races.length} races`);
  }
}

main().catch(console.error);

import ZAI from 'z-ai-web-dev-sdk';
import * as fs from 'fs';

async function main() {
  const zai = await ZAI.create();
  
  // Load real data
  const data = JSON.parse(fs.readFileSync('/home/z/my-project/download/abu_dhabi_real_data.json', 'utf-8'));
  
  const predictions: any[] = [];
  
  for (const race of data.races) {
    // Filter out reserves and non-runners
    const activeHorses = race.horses.filter((h: any) => !h.isNR && h.jockey && h.jockey !== '-');
    
    if (activeHorses.length === 0) continue;
    
    const prompt = `You are a horse racing expert. Analyze this race and provide predictions.

RACE ${race.race_number}: ${race.race_name}
Venue: Abu Dhabi Turf Club | Surface: Turf | Going: Good

HORSES (Number | Draw | Name | Country | Jockey | Trainer | Rating | Weight):
${activeHorses.map((h: any) => 
  `${h.number || '?'}. Draw ${h.draw || '?'}: ${h.name} (${h.country}) - Jockey: ${h.jockey}, Trainer: ${h.trainer || 'N/A'}, Rating: ${h.rating || 'Maiden'}, Weight: ${h.weight}kg`
).join('\n')}

Based on: rating, trainer form, jockey ability, draw advantage, provide predictions.

Return ONLY this JSON format:
{
  "nap": {"horse": "NAME", "reason": "Brief 1-sentence reason"},
  "next_best": {"horse": "NAME", "reason": "Brief 1-sentence reason"},
  "each_way": {"horse": "NAME", "reason": "Brief 1-sentence reason"},
  "top_3": ["1st Place Name", "2nd Place Name", "3rd Place Name"],
  "analysis": "2-3 sentence race analysis"
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
          horses_count: activeHorses.length,
          prediction: JSON.parse(jsonMatch[0])
        });
        console.log(`✓ Race ${race.race_number}: ${race.race_name} - ${activeHorses.length} horses`);
      } catch(e) {
        console.log(`✗ Parse error Race ${race.race_number}`);
      }
    }
  }
  
  // Save predictions
  const finalOutput = {
    meeting: data.meeting,
    predictions: predictions
  };
  
  fs.writeFileSync('/home/z/my-project/download/abu_dhabi_real_predictions.json', JSON.stringify(finalOutput, null, 2));
  
  console.log('\n=== PREDICTIONS GENERATED ===\n');
  console.log(JSON.stringify(predictions, null, 2));
}

main().catch(console.error);

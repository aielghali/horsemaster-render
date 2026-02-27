import ZAI from 'z-ai-web-dev-sdk';
import * as fs from 'fs';

async function main() {
  const zai = await ZAI.create();
  
  // Read from punters.com.au which has cleaner data
  const urls = [
    'https://www.punters.com.au/form-guide/horses/abu-dhabi-ae-20260227/race-1-wathba-stallions-cup-pure-arabian-stakes-race-1',
    'https://www.punters.com.au/form-guide/horses/abu-dhabi-ae-20260227/race-2-the-crescent-light-listed-stakes-race-2',
    'https://www.punters.com.au/form-guide/horses/abu-dhabi-ae-20260227/race-3-soil-of-the-union-stakes-race-3',
    'https://www.punters.com.au/form-guide/horses/abu-dhabi-ae-20260227/race-4-masar-almajd-mile-pure-arab-handicap-race-4'
  ];
  
  let allHtml = '';
  
  for (const url of urls) {
    try {
      const result = await zai.functions.invoke('page_reader', { url });
      allHtml += result.data?.html || '';
      console.log(`Fetched: ${url.split('/').pop()}`);
    } catch(e) {
      console.log(`Error: ${url} - ${e.message}`);
    }
  }
  
  // Use LLM to extract structured data
  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'system',
        content: `Extract ALL horse racing data from the HTML content. Find every horse with its:
- Number
- Draw position
- Name
- Jockey
- Trainer
- Rating
- Weight

Return as JSON with races array. Each race has: race_number, race_name, distance, time, and horses array.
Extract EVERY horse you can find. Be exhaustive.`
      },
      {
        role: 'user',
        content: `Extract from this HTML:\n\n${allHtml.substring(0, 50000)}`
      }
    ]
  });
  
  console.log('\n=== EXTRACTED DATA ===\n');
  console.log(completion.choices[0]?.message?.content);
}

main().catch(console.error);

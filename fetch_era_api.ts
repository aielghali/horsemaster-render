import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  const zai = await ZAI.create();
  
  // Use LLM to extract structured data from search snippets
  const searchResults = await zai.functions.invoke('web_search', {
    query: 'site:emiratesracing.com "27 February 2026" Abu Dhabi race horses jockeys trainers',
    num: 20
  });
  
  // Combine all snippets
  const allSnippets = searchResults.map((r: any) => r.snippet).join('\n');
  
  // Use LLM to extract and structure race data
  const completion = await zai.chat.completions.create({
    messages: [
      {
        role: 'system',
        content: `You are a horse racing data extraction expert. Extract all horse racing information from the provided text snippets.
        
Return a JSON object with this structure:
{
  "meeting": {
    "date": "27 February 2026",
    "venue": "Abu Dhabi Turf Club",
    "surface": "Turf",
    "going": "Good"
  },
  "races": [
    {
      "race_number": 1,
      "race_name": "Race Name",
      "distance": "1400m",
      "time": "16:00",
      "horses": [
        {
          "number": 1,
          "draw": 1,
          "name": "Horse Name",
          "jockey": "Jockey Name",
          "trainer": "Trainer Name",
          "rating": 85,
          "weight": 56
        }
      ]
    }
  ]
}

Only include data you can clearly extract. Use null for missing values.`
      },
      {
        role: 'user',
        content: `Extract horse racing data from these snippets:\n\n${allSnippets}`
      }
    ]
  });
  
  console.log(completion.choices[0]?.message?.content);
}

main().catch(console.error);

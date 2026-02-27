import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  const zai = await ZAI.create();
  
  // Search for specific race details
  const searches = [
    'Abu Dhabi February 27 2026 Race 1 Wathba Stallions Cup horses jockeys trainers draw',
    'Abu Dhabi February 27 2026 Race 2 Crescent Light Stakes entries',
    'Abu Dhabi February 27 2026 Race 3 Soil of the Union entries',
    'Abu Dhabi February 27 2026 Race 4 Masar Almajd Mile entries',
    'Abu Dhabi February 27 2026 Race 5 Darb Al Reeh Sprint entries',
    'Abu Dhabi February 27 2026 Race 6 Flash of Sand Handicap entries',
    'Abu Dhabi February 27 2026 Race 7 Majlis Mile entries'
  ];
  
  for (const query of searches) {
    const results = await zai.functions.invoke('web_search', { query, num: 3 });
    console.log(`\n=== ${query.split('Race')[1]?.split(' ')[0] || 'Unknown'} ===`);
    for (const r of results) {
      console.log(`- ${r.name}: ${r.snippet?.substring(0, 200)}`);
    }
  }
}

main().catch(console.error);

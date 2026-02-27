import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  const zai = await ZAI.create();
  
  // Fetch from racenet which has cleaner data
  const raceUrls = [
    'https://www.racenet.com.au/form-guide/horses/abu-dhabi-ae-20260227/race-1-wathba-stallions-cup-pure-arabian-stakes-race-1',
    'https://www.racenet.com.au/form-guide/horses/abu-dhabi-ae-20260227/race-2-the-crescent-light-listed-stakes-race-2'
  ];
  
  for (const url of raceUrls) {
    try {
      const result = await zai.functions.invoke('page_reader', { url });
      const html = result.data?.html || '';
      console.log(`\n=== ${url.split('/').pop()} ===`);
      
      // Extract runner data
      const runnerMatches = html.matchAll(/runner[^>]*>[\s\S]*?<a[^>]*>([^<]+)<\/a>/gi);
      const runners: string[] = [];
      for (const match of runnerMatches) {
        const name = match[1].trim();
        if (name && name.length > 2 && !runners.includes(name)) {
          runners.push(name);
        }
      }
      
      // Also try to find horse names in other patterns
      const horseNames = html.match(/horse-name[^>]*>([^<]+)</gi);
      if (horseNames) {
        console.log('Horse names:', horseNames.slice(0, 15).map(h => h.replace(/<[^>]+>/g, '')).join(', '));
      }
      
      // Find jockey info
      const jockeyInfo = html.match(/jockey[^>]*>([^<]+)</gi);
      if (jockeyInfo) {
        console.log('Jockey info found:', jockeyInfo.slice(0, 10).map(j => j.replace(/<[^>]+>/g, '')).join(', '));
      }
      
    } catch(e) {
      console.log(`Error: ${url} - ${e.message}`);
    }
  }
}

main().catch(console.error);

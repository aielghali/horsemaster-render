import ZAI from 'z-ai-web-dev-sdk';
import * as fs from 'fs';

async function main() {
  const zai = await ZAI.create();
  
  // Fetch each race individually for cleaner data
  const races: any[] = [];
  
  for (let i = 1; i <= 7; i++) {
    const url = `https://emiratesracing.com/racecard/2026-02-27/${i}/declarations`;
    console.log(`Fetching Race ${i}...`);
    
    try {
      const result = await zai.functions.invoke('page_reader', { url });
      const html = result.data?.html || '';
      
      // Extract table rows
      const rowMatches = html.match(/<tr[^>]*>[\s\S]*?<\/tr>/gi) || [];
      const cleanRows = rowMatches.map((r: string) => 
        r.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()
      ).filter((r: string) => r.includes('Jockey:') || r.includes('Rating:'));
      
      // Parse each horse
      const horses: any[] = [];
      for (const row of cleanRows) {
        // Extract horse data
        const numMatch = row.match(/^\s*(\d+)\s*(NR)?\s*\((\d+)\)|^\s*(\d+)\s+\((\d+)\)/);
        const nameMatch = row.match(/([A-Z][A-Z\s']+(\([A-Z]+\))?)\s*\((AE|FR|GB|US|QA|IT|SA)\)/);
        const jockeyMatch = row.match(/Jockey:\s*([^R]+?)(?:\s*Rating:|$)/);
        const ratingMatch = row.match(/Rating:\s*(\d+)/);
        const trainerMatch = row.match(/Trainer:\s*([A-Za-z\s]+?)(?:\s*Weight:|$)/);
        const weightMatch = row.match(/Weight:\s*(\d+)/);
        
        if (nameMatch) {
          horses.push({
            number: numMatch ? (numMatch[1] || numMatch[4]) : '',
            draw: numMatch ? (numMatch[3] || numMatch[5]) : '',
            name: nameMatch[1].trim(),
            country: nameMatch[3],
            jockey: jockeyMatch ? jockeyMatch[1].replace(/\|/g, '').trim() : '',
            rating: ratingMatch ? parseInt(ratingMatch[1]) : 0,
            trainer: trainerMatch ? trainerMatch[1].replace(/\|/g, '').trim() : '',
            weight: weightMatch ? parseInt(weightMatch[1]) : 57,
            isNR: row.includes('Non runner') || row.includes('NR')
          });
        }
      }
      
      // Get race name from page
      const raceNameMatch = html.match(/Race\s*${i}\s*-\s*([^<]+)/i);
      const raceName = raceNameMatch ? raceNameMatch[1].trim() : `Race ${i}`;
      
      races.push({
        race_number: i,
        race_name: raceName,
        horses: horses
      });
      
      console.log(`  Found ${horses.length} horses`);
      
    } catch(e: any) {
      console.log(`  Error: ${e.message}`);
    }
  }
  
  // Get race names from main page
  console.log('\nFetching race names...');
  const mainResult = await zai.functions.invoke('page_reader', {
    url: 'https://emiratesracing.com/racecard/2026-02-27/all/declarations'
  });
  
  const mainHtml = mainResult.data?.html || '';
  const raceNames = mainHtml.match(/Race\s*\d+\s*-\s*[^<]+/gi) || [];
  
  console.log('\nRace names found:', raceNames);
  
  // Create final data
  const finalData = {
    meeting: {
      date: '27 February 2026',
      venue: 'Abu Dhabi Turf Club',
      country: 'UAE',
      surface: 'Turf',
      going: 'Good'
    },
    races: races
  };
  
  // Save
  fs.writeFileSync('/home/z/my-project/download/abu_dhabi_real_data.json', JSON.stringify(finalData, null, 2));
  
  console.log('\n=== REAL DATA EXTRACTED ===\n');
  console.log(JSON.stringify(finalData, null, 2));
}

main().catch(console.error);

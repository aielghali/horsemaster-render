import ZAI from 'z-ai-web-dev-sdk';
import * as fs from 'fs';

async function main() {
  const zai = await ZAI.create();
  
  // Load existing data
  const data = JSON.parse(fs.readFileSync('/home/z/my-project/download/abu_dhabi_real_data.json', 'utf-8'));
  
  // Re-fetch Race 7 with more detail
  const result = await zai.functions.invoke('page_reader', {
    url: 'https://emiratesracing.com/racecard/2026-02-27/7/declarations'
  });
  
  const html = result.data?.html || '';
  const rowMatches = html.match(/<tr[^>]*>[\s\S]*?<\/tr>/gi) || [];
  
  console.log('Race 7 rows found:', rowMatches.length);
  
  // Parse horses from rows
  const horses: any[] = [];
  for (const row of rowMatches) {
    const cleanRow = row.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    if (cleanRow.includes('Jockey:') || cleanRow.includes('Rating:')) {
      const nameMatch = cleanRow.match(/([A-Z][A-Z\s']+(\([A-Z]+\))?)\s*\((AE|FR|GB|US|QA|IT|SA)\)/);
      const jockeyMatch = cleanRow.match(/Jockey:\s*([^R]+?)(?:\s*Rating:|$)/);
      const ratingMatch = cleanRow.match(/Rating:\s*(\d+)/);
      const trainerMatch = cleanRow.match(/Trainer:\s*([A-Za-z\s]+?)(?:\s*Weight:|$)/);
      const drawMatch = cleanRow.match(/\((\d+)\)/);
      const numMatch = cleanRow.match(/^\s*(\d+)/);
      
      if (nameMatch) {
        horses.push({
          number: numMatch ? numMatch[1] : '',
          draw: drawMatch ? drawMatch[1] : '',
          name: nameMatch[1].trim(),
          country: nameMatch[3],
          jockey: jockeyMatch ? jockeyMatch[1].replace(/\|/g, '').trim() : '',
          rating: ratingMatch ? parseInt(ratingMatch[1]) : 0,
          trainer: trainerMatch ? trainerMatch[1].replace(/\|/g, '').trim() : '',
          weight: 62
        });
      }
    }
  }
  
  console.log('Horses found:', horses.length);
  horses.forEach((h, i) => console.log(`${i+1}. ${h.name} (${h.country}) - Jockey: ${h.jockey}, Rating: ${h.rating}`));
  
  // Update Race 7
  data.races[6].horses = horses;
  data.races[6].race_name = 'The Majlis Mile';
  
  // Update all race names
  const raceNames = [
    'Wathba Stallions Cup',
    'The Crescent Light Stakes', 
    'Soil of the Union',
    'Masar Almajd Mile',
    'Darb Al Reeh Sprint',
    'The Flash of Sand Handicap',
    'The Majlis Mile'
  ];
  
  data.races.forEach((r: any, i: number) => {
    r.race_name = raceNames[i];
  });
  
  // Save updated data
  fs.writeFileSync('/home/z/my-project/download/abu_dhabi_real_data.json', JSON.stringify(data, null, 2));
  console.log('\nData updated and saved!');
}

main().catch(console.error);

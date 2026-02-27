import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  const zai = await ZAI.create();
  
  // Use SkyRacingWorld - they have cleaner data
  const result = await zai.functions.invoke('page_reader', {
    url: 'https://www.skyracingworld.com/form-guide/thoroughbred/united-arab-emirates/abu-dhabi/2026-02-27/runners-index'
  });
  
  console.log('Title:', result.data?.title);
  const html = result.data?.html || '';
  
  // Extract horse names and details using regex
  const horseMatches = html.matchAll(/horse[^>]*>([^<]+)<\/a>/gi);
  const horses: string[] = [];
  for (const match of horseMatches) {
    horses.push(match[1].trim());
  }
  
  console.log('\nHorses found:', [...new Set(horses)].slice(0, 50).join(', '));
  
  // Look for table data
  const tableData = html.match(/<table[^>]*>[\s\S]*?<\/table>/gi);
  if (tableData) {
    console.log('\nTables found:', tableData.length);
    // Extract text from first table
    const text = tableData[0].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
    console.log('\nTable content sample:', text.substring(0, 2000));
  }
}

main().catch(console.error);

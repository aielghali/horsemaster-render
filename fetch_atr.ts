import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  const zai = await ZAI.create();
  
  // Use AtTheRaces mobile site - usually lighter
  const urls = [
    'https://m.attheraces.com/racecard/Abu-Dhabi/27-February-2026/1200',
    'https://m.attheraces.com/racecard/Abu-Dhabi/27-February-2026/1230',
    'https://m.attheraces.com/racecard/Abu-Dhabi/27-February-2026/1300'
  ];
  
  for (const url of urls) {
    try {
      const result = await zai.functions.invoke('page_reader', { url });
      console.log(`\n=== ${url} ===`);
      // Extract text content
      const html = result.data?.html || '';
      // Get title and text
      console.log('Title:', result.data?.title);
      console.log('Content length:', html.length);
      // Print first 3000 chars of content
      console.log(html.substring(0, 3000));
    } catch(e) {
      console.log(`Error for ${url}:`, e.message);
    }
  }
}

main().catch(console.error);

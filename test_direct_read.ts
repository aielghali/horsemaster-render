import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  const zai = await ZAI.create();
  
  // Try different URLs
  const urls = [
    'https://emiratesracing.com/racecard/2026-02-27/1/declarations',
    'https://emiratesracing.com/racecard/2026-02-27/2/declarations',
    'https://emiratesracing.com/racecard/2026-02-27/all/declarations'
  ];
  
  for (const url of urls) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`Testing: ${url}`);
    console.log('='.repeat(60));
    
    try {
      const result = await zai.functions.invoke('page_reader', { url });
      const html = result.data?.html || '';
      
      console.log(`\n✓ Success! Content length: ${html.length} characters`);
      
      // Try to extract horse names using multiple patterns
      const patterns = [
        /horse[^>]*>([^<]+)</gi,
        /name[^>]*>([A-Z][A-Z\s]+)</gi,
        /class="[^"]*horse[^"]*"[^>]*>([^<]+)</gi,
        /jockey[^>]*>([^<]+)</gi,
        /trainer[^>]*>([^<]+)</gi
      ];
      
      console.log('\n--- Extracted Data ---');
      
      // Find horse rows/entries
      const rowMatches = html.match(/<tr[^>]*>[\s\S]*?<\/tr>/gi);
      if (rowMatches) {
        console.log(`Found ${rowMatches.length} table rows`);
        // Show first few rows
        for (let i = 0; i < Math.min(5, rowMatches.length); i++) {
          const text = rowMatches[i].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
          if (text.length > 10 && text.length < 500) {
            console.log(`Row ${i}: ${text.substring(0, 200)}`);
          }
        }
      }
      
      // Look for specific horse data patterns
      const horsePattern = /\d+\s*\(\d+\)\s*[A-Z][A-Z\s]+/g;
      const horseMatches = html.match(horsePattern);
      if (horseMatches) {
        console.log('\nHorse patterns found:', horseMatches.slice(0, 10).join(', '));
      }
      
    } catch(e: any) {
      console.log(`✗ Error: ${e.message}`);
    }
  }
}

main().catch(console.error);

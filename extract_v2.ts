import ZAI from 'z-ai-web-dev-sdk';
import * as fs from 'fs';

async function main() {
  const zai = await ZAI.create();
  
  // Read all races from the main page
  const result = await zai.functions.invoke('page_reader', {
    url: 'https://emiratesracing.com/racecard/2026-02-27/all/declarations'
  });
  
  const html = result.data?.html || '';
  
  // Extract all table rows and convert to clean text
  const rowMatches = html.match(/<tr[^>]*>[\s\S]*?<\/tr>/gi) || [];
  const cleanRows = rowMatches.map(r => r.replace(/<[^>]+>/g, ' | ').replace(/\s+/g, ' ').trim()).filter(r => r.length > 20);
  
  console.log('Found', cleanRows.length, 'rows');
  console.log('\nFirst 20 rows:\n');
  cleanRows.slice(0, 20).forEach((r, i) => console.log(`${i}: ${r.substring(0, 300)}`));
}

main().catch(console.error);

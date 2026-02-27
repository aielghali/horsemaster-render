import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  const zai = await ZAI.create();
  
  // Fetch race 1
  try {
    const r1 = await zai.functions.invoke('page_reader', {
      url: 'https://emiratesracing.com/racecard/2026-02-27/1/declarations'
    });
    console.log('=== RACE 1 ===');
    console.log(r1.data?.html?.substring(0, 5000) || 'No data');
  } catch(e) {
    console.log('Race 1 error:', e.message);
  }
  
  // Fetch race 2
  try {
    const r2 = await zai.functions.invoke('page_reader', {
      url: 'https://emiratesracing.com/racecard/2026-02-27/2/declarations'
    });
    console.log('\n=== RACE 2 ===');
    console.log(r2.data?.html?.substring(0, 5000) || 'No data');
  } catch(e) {
    console.log('Race 2 error:', e.message);
  }
}

main().catch(console.error);

import ZAI from 'z-ai-web-dev-sdk';

async function main() {
  const zai = await ZAI.create();
  
  // Search for Abu Dhabi race info
  const searchResults = await zai.functions.invoke('web_search', {
    query: 'Abu Dhabi horse racing February 27 2026 all races horses jockeys trainers',
    num: 15
  });
  
  console.log(JSON.stringify(searchResults, null, 2));
}

main().catch(console.error);

// npm i apify-client
import { ApifyClient } from 'apify-client';
import input from './input.json' with { type: 'json' };

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('datagrit/domain-whois-rdap-lookup').call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.length, 'records');
console.log(items[0]);

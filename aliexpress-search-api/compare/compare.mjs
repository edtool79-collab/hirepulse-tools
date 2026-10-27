export function compareSnapshots(before, after) {
  function index(rows) {
    if (!Array.isArray(rows)) throw new Error('Each export must be a JSON array of product rows.');
    if (rows.length > 50000) throw new Error('Please use exports with at most 50,000 rows.');
    const products = new Map(); let skipped = 0;
    for (const row of rows) {
      if (!row || typeof row !== 'object' || Array.isArray(row)) { skipped++; continue; }
      const id = row.product_id || (typeof row.url === 'string' && row.url.match(/\/item\/(\d+)\.html/)?.[1]);
      if (!id || !['query','currency','ship_to'].every(k => typeof row[k] === 'string' && row[k].trim())) { skipped++; continue; }
      const key = JSON.stringify([row.query.trim(), String(id), row.currency.trim().toUpperCase(), row.ship_to.trim().toUpperCase()]);
      products.set(key, {...row, product_id: String(id)});
    }
    return {products, skipped};
  }
  const old = index(before), current = index(after);
  const changes = [], observed = []; let comparable = 0, missingPrices = 0, absent = 0;
  for (const [key, b] of current.products) {
    const a = old.products.get(key);
    if (!a) { observed.push(b); continue; }
    comparable++;
    if (![a.price,b.price].every(v => typeof v === 'number' && Number.isFinite(v) && v >= 0)) { missingPrices++; continue; }
    if (a.price !== b.price) changes.push({query: b.query, product_id: b.product_id, title: b.title || b.product_id,
      currency: b.currency, ship_to: b.ship_to, previous_price: a.price, current_price: b.price,
      change: Number((b.price-a.price).toFixed(8)), previous_scraped_at: a.scraped_at || null,
      current_scraped_at: b.scraped_at || null});
  }
  for (const key of old.products.keys()) if (!current.products.has(key)) absent++;
  return {previous_products:old.products.size, current_products:current.products.size, comparable_products:comparable,
    price_changes:changes, newly_observed_listings:observed, not_observed_in_current_snapshot:absent,
    skipped_rows:old.skipped+current.skipped, comparable_products_without_both_prices:missingPrices,
    limitations:'Use identical search settings. Newly observed does not mean newly launched. Absence is not stock data. Listing prices can vary by variant and promotion. No sales velocity, delivery cost or profit is inferred.'};
}

if (typeof document !== 'undefined') {
  const form = document.querySelector('form');
  const earlier = document.querySelector('#earlier'), later = document.querySelector('#later');
  const status = document.querySelector('#status'), results = document.querySelector('#results');
  const submit = document.querySelector('#compare'), sample = document.querySelector('#sample');
  let lastResult;
  document.querySelectorAll('[data-goatcounter-click]').forEach(link=>link.addEventListener('click',()=>{
    window.goatcounter?.count({path:link.dataset.goatcounterClick,title:'AliExpress snapshot start',event:true});
  }));
  function cell(row, text) { const td=document.createElement('td'); td.textContent=String(text); row.append(td); }
  function render(result, isSample=false) {
    lastResult=result;
    const values=[result.comparable_products,result.price_changes.length,result.newly_observed_listings.length];
    document.querySelectorAll('[data-stat]').forEach((node,i)=>node.textContent=String(values[i]));
    const body=document.querySelector('tbody'); body.replaceChildren();
    for (const change of result.price_changes.slice(0,200)) {
      const row=document.createElement('tr');
      [change.title,change.previous_price,change.current_price,change.currency.toUpperCase(),change.ship_to.toUpperCase()].forEach(v=>cell(row,v));
      body.append(row);
    }
    document.querySelector('#empty').hidden=result.price_changes.length>0;
    document.querySelector('#table-wrap').hidden=result.price_changes.length===0;
    document.querySelector('#notes').textContent=`${result.previous_products} earlier and ${result.current_products} later product rows; ${result.not_observed_in_current_snapshot} not observed in the later snapshot. ${result.skipped_rows} rows skipped for missing IDs or comparison settings. ${result.comparable_products_without_both_prices} matched products lacked one or both prices. Showing up to 200 changes; the download contains all changes.`;
    document.querySelector('#sample-note').hidden=!isSample;
    status.textContent=isSample?'Loaded two saved validation exports. No Actor was run.':'Comparison complete. Your files were processed in this browser.';
    results.hidden=false; results.focus();
  }
  async function readFile(input) {
    const file=input.files?.[0];
    if (!file) throw new Error('Choose an earlier and a later JSON export.');
    if (file.size>10*1024*1024) throw new Error('Each file must be smaller than 10 MB.');
    return JSON.parse((await file.text()).replace(/^\uFEFF/,''));
  }
  form.addEventListener('submit',async event=>{
    event.preventDefault();submit.disabled=true;status.textContent='Reading your exports…';
    try {render(compareSnapshots(...await Promise.all([readFile(earlier),readFile(later)])));}
    catch(error) {results.hidden=true;status.textContent=error instanceof SyntaxError?'That file is not valid JSON. Export your Apify dataset as JSON and try again.':error.message;}
    finally {submit.disabled=false;}
  });
  sample.addEventListener('click',async()=>{
    sample.disabled=true;
    try {
      const arrays=await Promise.all(['earlier.json','later.json'].map(async url=>{
        const response=await fetch(url);if(!response.ok)throw new Error('The saved example could not be loaded.');return response.json();
      }));
      render(compareSnapshots(...arrays),true);
    } catch(error) {status.textContent=error.message;} finally {sample.disabled=false;}
  });
  document.querySelector('#download').addEventListener('click',()=>{
    if (!lastResult)return;
    const url=URL.createObjectURL(new Blob([JSON.stringify(lastResult,null,2)],{type:'application/json'}));
    const anchor=document.createElement('a');anchor.href=url;anchor.download='aliexpress-snapshot-comparison.json';anchor.click();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
}

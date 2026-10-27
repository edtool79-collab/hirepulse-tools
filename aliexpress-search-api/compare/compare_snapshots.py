"""Compare two saved AliExpress JSON exports locally; never calls any API.

Usage: python compare_snapshots.py previous.json current.json --output changes.json
Only compares equal query/product/currency/destination keys. Absence is not stock data.
"""
import argparse
import json
import math
from decimal import Decimal
from pathlib import Path


def index_products(rows):
    result={}
    for row in rows:
        if not isinstance(row,dict) or not row.get('product_id'):
            continue
        if not all(row.get(k) for k in ['query','currency','ship_to']):
            continue
        key=tuple(str(row[k]) for k in ['query','product_id','currency','ship_to'])
        result[key]=row
    return result


def compare(before,after):
    old,new=index_products(before),index_products(after)
    changes=[]
    for key in sorted(old.keys() & new.keys()):
        a,b=old[key],new[key]
        values=[a.get('price'),b.get('price')]
        if not all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) and v>=0 for v in values):
            continue
        if values[0]==values[1]:
            continue
        changes.append({'query':key[0],'product_id':key[1],'currency':key[2],'ship_to':key[3],
                        'previous_price':values[0],'current_price':values[1],
                        'change':float(Decimal(str(values[1]))-Decimal(str(values[0]))),
                        'previous_scraped_at':a.get('scraped_at'),'current_scraped_at':b.get('scraped_at'),
                        'url':b.get('url')})
    observed=[{'query':k[0],'product_id':k[1],'currency':k[2],'ship_to':k[3],'url':new[k].get('url')} for k in sorted(new.keys()-old.keys())]
    return {'previous_products':len(old),'current_products':len(new),'comparable_products':len(old.keys()&new.keys()),
            'price_changes':changes,'newly_observed_listings':observed,
            'not_observed_in_current_snapshot':len(old.keys()-new.keys()),
            'limitations':'Use the same search settings in both exports. Newly observed does not mean newly launched; absence does not mean out of stock. Listing prices can vary by variant and promotion. No sales velocity or profit is inferred.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('previous',type=Path);parser.add_argument('current',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    # Read-only inputs and exclusive output creation protect existing exports.
    rows=[json.loads(p.read_text(encoding='utf-8-sig')) for p in [args.previous,args.current]]
    if not all(isinstance(r,list) for r in rows): parser.error('Each input must be a JSON array exported from a dataset')
    result=compare(*rows)
    with args.output.open('x',encoding='utf8') as handle:
        json.dump(result,handle,ensure_ascii=False,indent=2)
    print(f"Compared {result['comparable_products']} products; {len(result['price_changes'])} listing-price changes. No network calls.")

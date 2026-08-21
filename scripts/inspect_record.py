import json
from pathlib import Path

payload = json.loads((Path(__file__).resolve().parents[1] / 'client/public/knowledge.json').read_text(encoding='utf-8'))
for record in payload['records']:
    if '464958325' in record['url']:
        print(json.dumps(record, ensure_ascii=False, indent=2))

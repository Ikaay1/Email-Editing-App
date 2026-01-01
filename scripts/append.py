import json

src = "datasets/new_shorten.jsonl"
dst = "datasets/tone.jsonl"

with open(src, "r", encoding="utf-8") as f_src, \
     open(dst, "a", encoding="utf-8") as f_dst:
    for line in f_src:
        if line.strip():
            record = json.loads(line)
            record["id"] = record["id"] + 122 
            f_dst.write(json.dumps(record, ensure_ascii=False) + "\n")
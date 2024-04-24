import json

input_file = "/files/20230814/知识问答文本.txt"
output_file = "/files/20230814/qa.jsonl"

with open(input_file, "r", encoding="utf-8") as infile:
    lines = infile.readlines()

data = []
i = 0
while i < len(lines):
    if lines[i].startswith("问："):
        question = lines[i][2:].strip()
        i += 1
        if i < len(lines) and lines[i].startswith("答："):
            answer = lines[i][2:].strip()
            entry = {
                "text": f"\n\nHuman: {question}\n\nAssistant: {answer}"
            }
            data.append(entry)
        i += 1
    else:
        i += 1

with open(output_file, "w", encoding="utf-8") as outfile:
    for entry in data:
        json.dump(entry, outfile, ensure_ascii=False)
        outfile.write("\n")

from generate import GenerateEmail

generateNewEmails = GenerateEmail("gpt-4.1")

output_file = f'datasets/new_lengthen.jsonl'


response = generateNewEmails.generate("generateShort", "", None, None)

response_text = response.choices[0].message.content.strip()

with open(output_file, "w", encoding="utf-8") as f:
    f.write(response_text)
    if not response_text.endswith("\n"):
        f.write("\n")

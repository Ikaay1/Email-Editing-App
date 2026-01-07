import json
from generate import GenerateEmail
import matplotlib.pyplot as plt

def evaluate(file_path, action, tone=None):
    emails = []
    with open(file_path, "r") as f:
        for line in f:
            emails.append(json.loads(line))
    
    emailsLength = len(emails)
    modelRatings = {"gpt-4.1": 0, "gpt-4o-mini": 0}

    for model in models:
        generateEmails = GenerateEmail(model)
        total = faithfulness = completeness = 0
        for email in emails:
            generatedEmail = generateEmails.generate(action, email["content"], tone, None).choices[0].message.content
            rawJudgedResponse = judgeEmails.generate("judge", email["content"], None, generatedEmail).choices[0].message.content
            parsedJudgedResponse = json.loads(rawJudgedResponse) if isinstance(rawJudgedResponse, str) else rawJudgedResponse

            total += parsedJudgedResponse["rating"]
            faithfulness += parsedJudgedResponse["faithfulness_rating"]
            completeness += parsedJudgedResponse["completeness_rating"]

        modelRatings[model] = {"rating": total/emailsLength, "faithfulness_rating": faithfulness/emailsLength, "completeness_rating": completeness/emailsLength}

    print(file_path, action, tone, modelRatings)
    key = action+"_"+tone if tone else action
    data[key] = {"count": emailsLength, "gpt-4.1": modelRatings["gpt-4.1"]["rating"], "gpt-4o-mini": modelRatings["gpt-4o-mini"]["rating"]}

def draw_graph(data):
    models = ["gpt-4.1", "gpt-4o-mini"]

    overall_totals = {m: 0.0 for m in models}

    for task in data.values():
        for m in models:
            overall_totals[m] += task[m] * task["count"]

    values = [overall_totals[m] for m in models]

    plt.figure()
    ax = plt.gca()

    ax.bar(models, values)

    ax.set_title("Overall Total Score Comparison")
    ax.set_ylabel("Total Score")

    lo, hi = min(values), max(values)
    pad = max(1.0, (hi - lo) * 0.35)
    ax.set_ylim(lo - pad, hi + pad)

    plt.tight_layout()
    plt.show()

    tasks = list(data.keys())

    totals = {
        task: {m: data[task][m] * data[task]["count"] for m in models}
        for task in tasks
    }

    for task in tasks:
        v1 = totals[task]["gpt-4.1"]
        v2 = totals[task]["gpt-4o-mini"]
        vals = [v1, v2]

        plt.figure()
        ax = plt.gca()
        ax.bar(models, vals)

        ax.set_title(f"TOTAL Score Comparison – {task}")
        ax.set_ylabel("Total Score")

        lo, hi = min(vals), max(vals)
        pad = max(1.0, (hi - lo) * 0.35)
        ax.set_ylim(lo - pad, hi + pad)

        plt.tight_layout()
        plt.show()



models = ["gpt-4o-mini", "gpt-4.1"]
judgeEmails = GenerateEmail("gpt-4.1")
data = {}

evaluate('datasets/lengthen.jsonl', "shorten")
evaluate('datasets/shorten.jsonl', "lengthen")
evaluate('datasets/tone.jsonl', "tone", "friendly")
evaluate('datasets/tone.jsonl', "tone", "sympathetic")
evaluate('datasets/tone.jsonl', "tone", "professional")
draw_graph(data)
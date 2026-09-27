
import os
from flask import Flask, request, render_template_string
from google import genai

app = Flask(__name__)

# Get Gemini API key from environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.8-flash"


def home_repair_detective(user_input):

    prompt = f"""
You are Home Repair Detective, an AI troubleshooting assistant.

User's home problem:
{user_input}

Analyze the problem carefully.

Give the answer using these sections:

1. DETECTIVE AGENT
- Problem Summary
- Possible Causes
- Important Questions

2. SOLUTION AGENT
- Safe Checks
- Suggested Next Steps

3. SAFETY AGENT
- Safety Warning
- When to Contact a Professional

Rules:
- Do not claim a definite diagnosis when there is not enough information.
- Give simple beginner-friendly explanations.
- Never recommend dangerous electrical, gas, fire, or structural repairs.
- If professional help is needed, clearly say so.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


HTML = """
<!DOCTYPE html>
<html>

<head>

    <title>Home Repair Detective</title>

    <style>

        body {
            font-family: Arial, sans-serif;
            background-color: #f5f3ff;
            margin: 0;
            padding: 40px;
        }

        .container {
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
        }

        h1 {
            text-align: center;
            color: #5b4bc4;
        }

        textarea {
            width: 100%;
            height: 150px;
            padding: 15px;
            box-sizing: border-box;
            border-radius: 10px;
            border: 1px solid #ccc;
            font-size: 16px;
        }

        button {
            display: block;
            margin: 20px auto;
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            background-color: #6c5ce7;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        .result {
            margin-top: 25px;
            padding: 20px;
            background-color: #faf9ff;
            border-radius: 10px;
            white-space: pre-wrap;
            line-height: 1.6;
        }

    </style>

</head>

<body>

<div class="container">

    <h1>🔧 Home Repair Detective</h1>

    <p>
        Describe your home problem and our AI agents will investigate it.
    </p>

    <form method="POST">

        <textarea
            name="problem"
            placeholder="Example: My ceiling fan is making a clicking sound."
            required
        ></textarea>

        <button type="submit">
            🔍 Investigate Problem
        </button>

    </form>

    {% if result %}

    <div class="result">
        {{ result }}
    </div>

    {% endif %}

    {% if error %}

    <div class="result">
        {{ error }}
    </div>

    {% endif %}

</div>

</body>

</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    error = ""

    if request.method == "POST":

        user_input = request.form.get("problem")

        try:
            result = home_repair_detective(user_input)

        except Exception as e:
            error = f"Something went wrong: {e}"

    return render_template_string(
        HTML,
        result=result,
        error=error
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )

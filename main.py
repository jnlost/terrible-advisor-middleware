from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# --------------------------
# Create Flask app
# --------------------------
app = Flask(__name__)
CORS(app)

# --------------------------
# Load OpenAI API key
# --------------------------
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    print("❌ WARNING: OPENAI_API_KEY is not set!")

# --------------------------
# /getAdvice route
# --------------------------
@app.route("/getAdvice", methods=["POST"])
def get_advice():
    data = request.json
    user_text = data.get("message", "")

    system_prompt = """
    You are a silly, chaotic Roblox NPC called "Terrible Advisor".
    Always give obviously bad advice, funny and safe.
    Keep responses under 100 characters.
    """

    try:
        # ChatCompletion call compatible with OpenAI 1.106.1
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            max_tokens=80,
            temperature=1
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        # Log full error to Render logs
        print("❌ OpenAI Error:", repr(e))
        return jsonify({"reply": "Oops! My advice machine is jammed."})

# --------------------------
# Run Flask app
# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

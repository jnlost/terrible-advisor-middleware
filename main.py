from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# --------------------------
# Flask app
# --------------------------
app = Flask(__name__)
CORS(app)

# --------------------------
# OpenAI API key
# --------------------------
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    print("❌ WARNING: OPENAI_API_KEY not set!")

# --------------------------
# /getAdvice endpoint
# --------------------------
@app.route("/getAdvice", methods=["POST"])
def get_advice():
    data = request.json
    user_text = data.get("message", "")

    system_prompt = """
    You are a chaotic Roblox NPC called 'Terrible Advisor'.
    Always give silly, obviously bad advice that is safe to follow.
    Keep answers short, playful, and under 100 characters.
    """

    try:
        # Call OpenAI ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            max_tokens=80,
            temperature=1
        )

        # Log full response for debugging
        print("✅ OpenAI raw response:", response)

        # Extract reply text
        reply = response.choices[0].message.content.strip()
        print("✅ Reply extracted:", reply)

        return jsonify({"reply": reply})

    except Exception as e:
        # Print full error to logs
        print("❌ OpenAI Error:", repr(e))
        return jsonify({"reply": "Oops! My advice machine is jammed."})

# --------------------------
# Run the app
# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

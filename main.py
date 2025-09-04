from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# 1️⃣ Create Flask app
app = Flask(__name__)
CORS(app)

# 2️⃣ Load OpenAI API key from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 3️⃣ Define /getAdvice route
@app.route("/getAdvice", methods=["POST"])
def get_advice():
    data = request.json
    user_text = data.get("message", "")

    system_prompt = """
    You are 'The Terrible Advisor' NPC in a Roblox game.
    Always give funny, obviously bad but safe advice.
    Keep responses short and playful.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            max_tokens=80,
            temperature=1
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        # Log the real error in Render logs
        print("❌ OpenAI Error:", repr(e))
        return jsonify({"reply": "Oops! My advice machine is jammed."})

# 4️⃣ Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

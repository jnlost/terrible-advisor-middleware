from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# OpenAI API key stored securely as environment variable in Render
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/getAdvice", methods=["POST"])
def get_advice():
    data = request.json
    user_text = data.get("message", "")

    system_prompt = """
    You are 'The Terrible Advisor' NPC in a Roblox game.
    Give obviously silly, impractical, safe advice about snacks, school, fashion, chores, or video games.
    Never give real health, crime, money, or dangerous advice.
    Keep responses under 180 characters.
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
        return jsonify({"reply": "Oops! My advice machine is jammed."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

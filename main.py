from flask import Flask, request, jsonify
import openai, os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/getAdvice", methods=["POST"])
def get_advice():
    user_text = request.json.get("message", "")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":user_text}],
            max_tokens=80
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        print("❌ OpenAI Error:", repr(e))
        return jsonify({"reply":"Oops! My advice machine is jammed."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

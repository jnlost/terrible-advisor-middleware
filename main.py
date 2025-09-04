@app.route("/getAdvice", methods=["POST"])
def get_advice():
    try:
        data = request.json
        user_message = data.get("message", "")

        system_prompt = "You are a terrible life coach. Always give bad advice."

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        # 👇 log the real error so you can see it in Render’s logs
        print("Error talking to OpenAI:", str(e))
        return jsonify({"reply": "Oops! My advice machine is jammed."})

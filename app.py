from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    destination = request.form["destination"]
    days = request.form["days"]
    budget = request.form["budget"]
    interests = request.form["interests"]

    prompt = f"""
     You are an expert travel planner.

     Create a detailed {days}-day itinerary for {destination}.

     Budget: ₹{budget}
     Interests: {interests}

     
     Formatting Instructions:
     - Do NOT use * bullets.
     - Use 📅 for each day heading.
     - Use 📍 for all itinerary points.
     - Use 💰 for budget information.
     - Use 🎒 for packing suggestions.
     - Make the output visually attractive and easy to read.
     """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    itinerary = response.choices[0].message.content

    return render_template(
        "result.html",
        itinerary=itinerary
    )


if __name__ == "__main__":
    app.run(debug=True)
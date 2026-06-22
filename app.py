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
    Create a {days}-day travel itinerary.

    Destination: {destination}
    Budget: ₹{budget}
    Interests: {interests}

    Include:
    1. Day-wise plan
    2. Estimated expenses
    3. Packing suggestions
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
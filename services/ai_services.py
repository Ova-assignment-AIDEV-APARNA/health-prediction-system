from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def predict_health(glucose, haemoglobin, cholesterol):

    prompt = f"""
    Analyze blood test values.

    Glucose: {glucose}
    Haemoglobin: {haemoglobin}
    Cholesterol: {cholesterol}

    Return only ONE short sentence.
    Maximum 15 words.
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        print("Gemini Response:")
        print(response.text)

        return response.text.strip()

    except Exception as e:

        print("Gemini Error:", e)

        # Intelligent fallback
        if glucose > 140:
            return "High glucose levels detected. Medical review recommended."

        elif haemoglobin < 12:
            return "Low haemoglobin detected. Possible anemia risk."

        elif cholesterol > 200:
            return "Elevated cholesterol levels. Lifestyle changes may be beneficial."

        else:
            return "Blood parameters appear within normal ranges."
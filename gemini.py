# gemini.py
import os
import json
import google.generativeai as genai

# Configure Gemini with your API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Select a supported model (confirmed available)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

def get_focus_tip():
    prompt = (
        "Give me 1 unique and scientifically backed distraction management or focus-enhancing technique. "
    "Return the response in valid JSON format as: "
    "{'title': '...', 'description': '...', 'category': '...'} "
    "Do not repeat the Pomodoro Technique. Avoid repetition. Make sure the responses are not longer than 4 sentences and 70 words. "
    "Vary the title and method each time."
    )

    try:
        # Generate content from Gemini
        response = model.generate_content(prompt, generation_config={"temperature": 1.0})      
        # Extract response safely (avoid deprecated .text)
        content = response.candidates[0].content.parts[0].text.strip()
        print("Gemini raw content:", content)  # Optional for debugging

        # Extract valid JSON from response text
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            json_text = content[start:end + 1]
            return json.loads(json_text)

        raise ValueError("JSON structure not found in response.")

    except Exception as e:
        print("Gemini error:", e)
        return {
            "title": "Deep Breathing",
            "description": "Breathe deeply for 2 minutes to reset your focus.",
            "category": "Mindfulness"
        }

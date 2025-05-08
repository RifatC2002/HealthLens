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
def get_mood_routine(mood):
    prompt = (
        f"Suggest a simple fitness routine for someone feeling {mood}. Suggest activities that are common and known to general people "
        "Keep it short, and return only the routine string. Example: '10-min walk, 15 squats, 5 deep breaths'"
    )

    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        response = model.generate_content(prompt, generation_config={"temperature": 1.0})
        return response.text.strip()
    except Exception:
        return "10-min walk, 15 squats, 5 deep breaths"

def generate_routine_based_on_inputs(height, weight, goal_weight, duration, duration2, daily_hours):
    import json

    prompt = (
    f"You're a fitness coach. Generate a 7-day workout routine based on:\n"
    f"Height: {height} cm, Weight: {weight} kg, Goal: {goal_weight} kg, "
    f"Duration: {duration} weeks, Duration2: {duration2} weeks, "
    f"Time per day: {daily_hours} hrs.\n\n"
    f"Return ONLY the following JSON list format:\n"
    f"[['Monday', '7 AM', 'Core'], ['Tuesday', '8 AM', 'Lower body'], ..., ['Sunday', 'Rest', 'No workout']]\n\n"
    f"No explanation or markdown."
)


    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

    try:
        response = model.generate_content(prompt, generation_config={"temperature": 1.0})
        content = response.parts[0].text.strip()
        return json.loads(content)
    except Exception as e:
        print(f"Gemini routine fallback used due to: {e}")
        return [
            ['Monday', '7 AM', '20 min Cardio'],
            ['Tuesday', '8 AM', 'Upper Body Workout'],
            ['Wednesday', '7 AM', 'Yoga & Core'],
            ['Thursday', '8 AM', 'Lower Body Workout'],
            ['Friday', '7 AM', 'Stretch + Cardio'],
            ['Saturday', '8 AM', 'Fun Activity or Walk'],
            ['Sunday', 'Rest', 'Recovery Day'],
        ]


def generate_fitness_challenge():
    prompt = (
            "Generate a fitness challenge which might be useful for a beginner level user. "
            "Make sure the title and description is different from the previous responses. "
            "Respond only in JSON format: {\"title\": \"...\", \"description\": \"...\"}. "
            "Avoid repeating phrases or names. No explanation or markdown."
        )

    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt, generation_config={"temperature": 1.0})
        content = response.candidates[0].content.parts[0].text.strip()
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            return json.loads(content[start:end + 1])
    except Exception as e:
        print("Challenge generation fallback:", e)
        return {
            "title": "Jumping Jacks Blast",
            "description": "Do 30 jumping jacks to get your heart rate up!"
        }

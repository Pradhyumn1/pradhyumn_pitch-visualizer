from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.text_processor import TextProcessor
from utils.prompt_engineer import PromptEngineer
import urllib.parse
import hashlib

load_dotenv()

app = Flask(__name__)

# OpenAI client – safe even if key is missing or invalid
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key and api_key.startswith("sk-") else None

text_processor = TextProcessor()


def get_placeholder_image(prompt: str) -> str:
    """Deterministic Unsplash image based on prompt."""
    seed = hashlib.md5(prompt.encode()).hexdigest()[:8]
    keyword = prompt.split(",")[0].strip().replace(" ", "+")
    return f"https://source.unsplash.com/1024x1024/?{keyword}&sig={seed}"

def generate_image(prompt: str):
    if client:
        try:
            print(f"Generating with DALL·E 3: {prompt[:80]}...")
            resp = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return resp.data[0].url
        except Exception as e:
            print(f"DALL·E failed → using placeholder: {e}")
            # Fall through to placeholder
    else:
        print("No OpenAI key → using placeholder")

    return get_placeholder_image(prompt)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_storyboard():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        style = data.get("style", "digital art")

        if not text:
            return jsonify({"error": "Please enter a story"}), 400

        scenes = text_processor.segment_narrative(text)
        if len(scenes) < 3:
            return jsonify({"error": "Need at least 3 sentences"}), 400

        engineer = PromptEngineer(style=style)
        storyboard = []

        for i, scene in enumerate(scenes):
            prompt = engineer.enhance_prompt(scene)
            print(f"\nScene {i+1}: {scene[:70]}...")
            print(f"Prompt: {prompt}")

            image_url = generate_image(prompt)

            storyboard.append({
                "text": scene,
                "prompt": prompt,
                "image_url": image_url
            })

        return jsonify({"storyboard": storyboard})

    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Something went wrong. Try again."}), 500

if __name__ == "__main__":
    import socket
    from contextlib import closing

    def free_port(start=5000):
        for p in range(start, start + 100):
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
                if s.connect_ex(("127.0.0.1", p)) != 0:
                    return p
        raise RuntimeError("No free ports")

    port = free_port()
    print(f"\nPitch Visualizer → http://localhost:{port}\n")
    app.run(debug=True, port=port)


# from flask import Flask, render_template, request, jsonify
# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from utils.text_processor import TextProcessor
# from utils.prompt_engineer import PromptEngineer
# import hashlib 
# import urllib.parse 

# load_dotenv()

# app = Flask(__name__)

# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key) if api_key and api_key.startswith("sk-") else None

# text_processor = TextProcessor()


# def get_placeholder_image(prompt: str) -> str:
#     hash_value = hashlib.md5(prompt.encode()).hexdigest()
    
#     keyword = "API_Error" 
#     if len(prompt.split()) > 2:
#         keyword = "+".join(prompt.split()[:3]) 
    
#     encoded_keyword = urllib.parse.quote_plus(keyword)

#     return f"https://via.placeholder.com/1024x1024/d3d3d3/555555?text={encoded_keyword}"

# def generate_image(prompt: str):
#     if client:
#         try:
#             print(f"Generating with DALL·E 3: {prompt[:80]}...")
#             resp = client.images.generate(
#                 model="dall-e-3",
#                 prompt=prompt,
#                 size="1024x1024",
#                 quality="standard",
#                 n=1,
#             )
#             return resp.data[0].url
#         except Exception as e:
#             print(f"DALL·E failed → using online placeholder: {e}")
#     else:
#         print("No OpenAI key → using online placeholder")

#     return get_placeholder_image(prompt)

# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/generate", methods=["POST"])
# def generate_storyboard():
#     try:
#         data = request.get_json()
#         text = data.get("text", "").strip()
#         style = data.get("style", "digital art")

#         if not text:
#             return jsonify({"error": "Please enter a story"}), 400

#         scenes = text_processor.segment_narrative(text)
#         if len(scenes) < 3:
#             return jsonify({"error": "Need at least 3 sentences"}), 400

#         engineer = PromptEngineer(style=style)
#         storyboard = []

#         for i, scene in enumerate(scenes):
#             prompt = engineer.enhance_prompt(scene)
#             print(f"\nScene {i+1}: {scene[:70]}...")
#             print(f"Prompt: {prompt}")

#             image_url = generate_image(prompt)

#             storyboard.append({
#                 "text": scene,
#                 "prompt": prompt,
#                 "image_url": image_url
#             })

#         return jsonify({"storyboard": storyboard})

#     except Exception as e:
#         print(f"Server error: {e}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({"error": "Something went wrong. Try again."}), 500

# if __name__ == "__main__":
#     import socket
#     from contextlib import closing

#     def free_port(start=5000):
#         for p in range(start, start + 100):
#             with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
#                 if s.connect_ex(("127.0.0.1", p)) != 0:
#                     return p
#         raise RuntimeError("No free ports")

#     port = free_port()
#     print(f"\nPitch Visualizer → http://localhost:{port}\n")
    
#     if not client:
#         print("="*50)
#         print("WARNING: OpenAI API key not found or invalid.")
#         print("App will use online placeholders for images.")
#         print("Please ensure your .env file has OPENAI_API_KEY=sk-YOUR_KEY_HERE")
#         print("and that your OpenAI account has sufficient credits.")
#         print("="*50)
#     else:
#         print("✓ OpenAI API key loaded successfully. Attempting DALL·E 3 generation.")
        
#     app.run(debug=True, port=port)
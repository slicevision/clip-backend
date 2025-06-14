from flask import Flask, request, jsonify, send_file
import os
import subprocess
import uuid
import shutil
print("FFmpeg path:", shutil.which("ffmpeg"))

app = Flask(__name__)

@app.route("/")
def index():
    return "FFmpeg clip backend is running!"

@app.route("/clip", methods=["POST"])
def clip_video():
    try:
        data = request.json
        source_url = data["source_url"]
        clips = data["clips"]
        clip_paths = []

        for i, clip in enumerate(clips):
            start = clip["startTime"]
            end = clip["endTime"]
            output = f"clip_{uuid.uuid4()}_{i}.mp4"
            command = [
                "ffmpeg", "-y", "-ss", str(start), "-i", source_url,
                "-t", str(end - start), "-c", "copy", output
            ]
            subprocess.run(command, check=True)
            clip_paths.append(output)

        return jsonify({"clips": clip_paths})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

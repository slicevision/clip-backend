from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import subprocess
import requests
import os
import uuid

app = Flask(__name__)
CORS(app, origins=["https://slice-vision-streamer.lovable.app"])

@app.route('/')
def hello():
    return "✅ Backend is running!"

@app.route('/clip', methods=['POST'])
def clip_video():
    data = request.json
    source_url = data.get("source_url")
    clips = data.get("clips")

    if not source_url or not clips:
        return jsonify({"error": "Missing source_url or clips"}), 400

    try:
        input_path = f"/tmp/input_{uuid.uuid4()}.mp4"
        with open(input_path, 'wb') as f:
            f.write(requests.get(source_url).content)

        segment_paths = []
        for i, clip in enumerate(clips):
            start = clip["startTime"]
            end = clip["endTime"]
            duration = end - start
            segment_path = f"/tmp/segment_{i}.mp4"
            subprocess.run([
                "ffmpeg", "-ss", str(start), "-i", input_path, "-t",
                str(duration), "-c", "copy", segment_path
            ], check=True)
            segment_paths.append(segment_path)

        list_path = "/tmp/list.txt"
        with open(list_path, "w") as f:
            for path in segment_paths:
                f.write(f"file '{path}'\n")

        output_path = f"/tmp/output_{uuid.uuid4()}.mp4"
        subprocess.run([
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_path, "-c",
            "copy", output_path
        ], check=True)

        return send_file(output_path,
                         as_attachment=True,
                         download_name="clip.mp4")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("✅ Flask server avviato")
    app.run(debug=True, host="0.0.0.0", port=8000)

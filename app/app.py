from flask import Flask, jsonify, request

app = Flask(__name__)

notes = []


@app.get("/")
def home():
    return jsonify({
        "service": "notes-api",
        "status": "running"
    })


@app.get("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200


@app.get("/notes")
def get_notes():
    return jsonify(notes), 200


@app.post("/notes")
def create_note():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "text is required"}), 400

    note = {
        "id": len(notes) + 1,
        "text": data["text"]
    }

    notes.append(note)

    return jsonify(note), 201


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

#!/usr/bin/env python3
"""Flask UI for the markdown → Substack converter.

Run:
    python3 app.py
Then open http://localhost:5051
"""

from flask import Flask, render_template, request, jsonify, Response

from convert import md_to_html

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    md_text = ""

    if "file" in request.files and request.files["file"].filename:
        md_text = request.files["file"].read().decode("utf-8")
    else:
        md_text = (request.form.get("markdown") or "").strip()

    if not md_text:
        return jsonify({"error": "no markdown provided"}), 400

    html = md_to_html(md_text)
    return jsonify({
        "html": html,
        "word_count": len(md_text.split()),
    })


@app.route("/download", methods=["POST"])
def download():
    md_text = (request.form.get("markdown") or "").strip()
    filename = request.form.get("filename") or "post"
    if not md_text:
        return "no markdown provided", 400

    html = md_to_html(md_text)
    safe = "".join(c for c in filename if c.isalnum() or c in "-_") or "post"
    return Response(
        html,
        mimetype="text/html",
        headers={"Content-Disposition": f'attachment; filename="{safe}.html"'},
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5051)

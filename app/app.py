#!/usr/bin/env python
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="App")


@app.route("/generate_phrase", methods=["POST"], endpoint="generate_phrase")
def generate_phrase():
    data = request.form

    if "input_string" not in data:
        return jsonify({"error": "Input string not provided"}), 400

    input_string = data["input_string"]
    random_integer = np.random.randint(1, 11)

    if is_palindrome(input_string):
        phrase = f"I would like {random_integer} {input_string} please. {input_string} IS a palindrome."
    else:
        phrase = f" I would like {random_integer} {input_string} please. {input_string} is NOT a palindrome."

    is_palindrome_result = is_palindrome(input_string)

    return jsonify({"phrase": phrase, "is_palindrome": is_palindrome_result})


def is_palindrome(s):
    s = s.lower()
    return s == s[::-1]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

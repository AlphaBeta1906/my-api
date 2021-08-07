from flask import Flask, jsonify, abort, render_template

app = Flask(__name__)


@app.errorhandler(401)
def _401(e):
    return (
        jsonify(
            {
                "message": (
                    "dont use hindu arabic number(1,2,3..) use roman number(I,X,V...)"
                    " instead"
                ),
                "status": 401,
            }
        ),
        401,
    )


@app.errorhandler(404)
def _404(e):
    return (
        jsonify({"message": "url not found or empty/invalid parameter", "status": 404}),
        404,
    )


@app.errorhandler(500)
def _500(e):
    return jsonify({"message": "server eror", "status": 500}), 500


def text_to_ascii(text) -> list:
    return [ord(char) for char in text]


def ascii_to_text(_ascii) -> str:
    _ascii = _ascii.split(" ")
    text = [chr(int(char)) for char in _ascii]
    return "".join(text)


def caesar_encrypt(text) -> str:
    result = ""
    for char in text:
        print(char.isdigit())
        if not char.isspace():
            result += chr((ord(char) + 4 - 97) % 26 + 97)
        else:
            continue
        if char.isdigit():
            abort(401)
            break
    return result


def caesar_decrypt(text) -> str:
    result = ""
    for char in text:
        if not char.isspace():
            result += chr((ord(char) + 4 - 97) % 26 + 97)
        elif char.isdigit():
            abort(401)
            break
        else:
            continue
    return result


@app.get("/")
def main():
    return render_template("index.html")


@app.get("/text_to_ascii/<string:text>")
def convert_text(text):
    result = [str(ch) for ch in text_to_ascii(text)]
    return (
        jsonify(
            {"plain_text": text, "result_to_ascii": " ".join(result), "status": 200}
        ),
        200,
    )


@app.get("/ascii_to_text/<string:_ascii>")
def convert_ascii(_ascii):
    result = ascii_to_text(_ascii)
    return jsonify({"ascii": _ascii, "result_to_plain_text": result, "status": 200})


@app.get("/caesar_encrypt/<string:text>")
def encrypt_caesar(text):
    result = caesar_encrypt(text)
    return jsonify({"plain_text": text, "result": result, "status": 200}), 200


@app.get("/caesar_decrypt/<string:text>")
def decrypt_caesar(text):
    result = caesar_decrypt(text)
    return jsonify({"plain_text": text, "result": result, "status": 200}), 200


app.run(debug=True)

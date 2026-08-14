from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Hola desde Render"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"ARRANCANDO EN {port}", flush=True)
    app.run(host="0.0.0.0", port=port)
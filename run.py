"""Entry point untuk menjalankan Task Tracker secara lokal."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug dimatikan agar tidak membuka Werkzeug debugger (risiko keamanan)
    app.run(host="127.0.0.1", port=5000, debug=False)

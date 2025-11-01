from src import app
import os

if __name__ == '__main__':
    # Docker環境では0.0.0.0にバインドする必要がある
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'

    app.run(host=host, port=port, debug=debug)

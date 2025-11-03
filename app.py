from src import app
import os

if __name__ == '__main__':
    # Docker環境では0.0.0.0にバインドする必要がある
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 8080))
    debug = True

    app.run(host=host, port=port, debug=debug)

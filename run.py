from app import create_app
from app.utils.config import Config
from flask_cors import CORS
 
app = create_app()
CORS(app)
 
if __name__ == "__main__":
    config = Config()
    app.run(host=config.HOST, port=config.PORT, debug=True) 
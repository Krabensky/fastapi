import os

import uvicorn
# from src.main import app

if __name__ == '__main__':
	uvicorn.run( "src.main:app", host="0.0.0.0", port=os.getenv( "PORT", default=8000 ), log_level="info" )
	
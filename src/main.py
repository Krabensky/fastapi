from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount( "/static", StaticFiles( directory="src/routing/static" ), name="static" )
# app.mount( '/', StaticFiles( directory='public', html=True ) )

templates = Jinja2Templates( directory='src/routing/templates' )



from .routing.routes import *


# from fastapi import Request
# @app.get('/')
# def home( request: Request ):
#     return { 'one': 1 }

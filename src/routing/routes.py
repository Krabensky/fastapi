from fastapi import Request, Depends, Response, HTTPException, Cookie
# from fastapi.responses import RedirectResponse
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND

from sqlalchemy.orm import Session


from ..main import app, templates

from ..db_func.tolling_user import *

from datetime import date


from authx import AuthX, AuthXConfig

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


# /login
# /transaction
# /main


@app.get( "/" )
def redir():
	# return RedirectResponse( '/main' )
    # return templates.TemplateResponse(
	# 	'login.html',
	# 	{'request': 123,}
	# 	)
	return templates.TemplateResponse(
			'index.html',
			{
				'request': 123,
			}
		)



@app.get( '/regist_window' )
def regist_window():
	url = app.url_path_for('home')
	return templates.TemplateResponse(
			'login.html',
			{
				'request': 123,
			}
		)

# random_project/src/main.py
@app.get( '/auth_window' )
def regist_window():
	return templates.TemplateResponse(
			'login.html',
			{
				'request': 123,
			}
		)



@app.post( '/auth' )
def auth( username: str, password: str, response: Response, db_session: Session=Depends( db_engine ) ):
	users = db_session.query(
		User
		).all()
	for user in users:
		if user.username == username and user.password == password:
			token = security.create_access_token( uid=username )
			response.set_cookie( config.JWT_ACCESS_COOKIE_NAME, token )
			return templates.TemplateResponse(
				'main.html',
				{
					"access_token": token,
					# "in_or_out": in_or_out,
				}
			)
		else:
			return templates.TemplateResponse(
				'login.html',
			)
	# raise HTTPException(401, detail={"message": "Bad credentials"})





@app.post( '/regist' )
def regist( username: str, password: str, response: Response, db_session: Session=Depends( db_engine ) ):
	if_exist = db_session.query( User ).filter( User.username == username ).one()

	if if_exist:
		return templates.TemplateResponse(
			'error_of_login.html',
		)
	
	else:
		import random
		number_of_balance = random(0, 1000000)

		now = date.today()
		new_user = User( username=username, password=password, date_of_reg=now, number_of_balance=number_of_balance )

		new_ballanse = Ballanse( money=1000 )

		token = security.create_access_token( uid=username )

		new_token = Token_Auth( token=token, last_activity=now )

		db_session.add( new_user, new_ballanse, new_token )
		db_session.commit()
		db_session.close()

		response.set_cookie( config.JWT_ACCESS_COOKIE_NAME, token )

		

		return templates.TemplateResponse(
			'main.html',
			{
				"access_token": token,
				"money": new_ballanse,
				"username": User.username,
			}
		)
	
	

@app.post( '/login' )
def login( username: str, password: str, response: Response, db_session: Session=Depends( db_engine ) ):
	if username == None:
		token = security.create_access_token( uid=username )
		response.set_cookie( config.JWT_ACCESS_COOKIE_NAME, token )
		return templates.TemplateResponse(
			'main.html',
			{
				"access_token": token,
				# "in_or_out": in_or_out,
			}
		)
	else:
		return templates.TemplateResponse(
			'error_of_login.html',
		)

	

 
@app.get( '/history' )
def history( request: Request, db_session: Session=Depends( db_engine ), dependencies=[ Depends( security.access_token_required ) ] ):
	trans_list = db_session.query( Ballanse )
	return templates.TemplateResponse(
		'trans_list.html',
		{
			'request': request,
			'trans_list': trans_list,
		}
	)


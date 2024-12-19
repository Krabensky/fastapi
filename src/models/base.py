from configur import Config 

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship

from sqlalchemy import Column, Integer, String, Text, JSON, BOOLEAN, Numeric, Date, ForeignKey


engine = create_engine( Config.database( ), echo=True )

Session = sessionmaker( bind=engine, autocommit=False )
session = Session( )


class Base( DeclarativeBase ):
	pass


class User( Base ):
	__tablename__ = 'User_data'

	id = Column( 'id', Integer, primary_key=True )
	username = Column( 'username', Text )
	password = Column( 'password', Text )
	# phone = Column( 'user_phone', Text )
	date_of_reg = Column( 'date_of_reg', Date )

	number_of_balance = relationship( "history_of_transactions")

	bal = relationship( "User_money", backref='User_data', uselist=False )
	moneys = relationship( "tokens", backref='User_data', uselist=False )


class Ballanse( Base ):
	__tablename__ =  'User_money'

	id = Column( 'id', Integer, primary_key=True )
	money = Column( 'money', Numeric )

	number_of_balance = Column( 'number_of_balance', Integer, ForeignKey( 'User_data.id' ) )
	


class Transaction( Base ):
	__tablename__ = 'history_of_transactions'

	id = Column( 'id', Integer, primary_key=True )
	from_user = ( 'user_id_from', Integer )
	to_user = Column( 'user_id_to', Integer )
	sum_of = Column( 'sum_of_transaction', Numeric )
	date_of_trans = Column( 'date_of_trans', Date )

	number_of_user = Column( Integer, ForeignKey( 'User_data.id' ) )
	


class Token_Auth( Base ):
	__tablename__ =  'tokens'

	id = Column( 'id', Integer, primary_key=True )
	token = Column( 'user_token', Text  )
	last_activity = Column( 'date_last_activity', Date )

	user_id = Column( Integer, ForeignKey( 'User_data.id' ) )






Base.metadata.create_all( bind=engine )
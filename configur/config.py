
class Config( ):

	def database( ):
		
		dialect="postgresql"
		driver="psycopg2"
		user="pguser"
		password="1111"	 	#FIXME
		host="127.0.0.1"	#FIXME
		port="5432"		 	#FIXME
		database="pipa"	 	#FIXME
		
		db_link = f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}"

		return db_link
		

	def token( ):
		token = '6394949019:AAEAc5Hy5JAVwpVZ6ChmnjZqCU_wNPc1XuY'	#FIXME
		return token
	
	def rabbit( ):
		host = "localhost"	  #DELLETME #FIXME
		return host
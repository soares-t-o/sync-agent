from os import getenv

URL_DB = getenv('URL_DB', 'mongodb://localhost:27017/')
DATABASE = getenv('DATABASE_NAME', 'e-cattle')
TOKEN = getenv('TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2RlRmFybSI6MSwiaWF0IjoxNjE5NzI0MTYwLCJleHAiOjE3Nzc1MTIxNjB9.6Sg4ozy9v_CPzYiB1KxjyNtw3wz5LmKR6TPafa3XWwg')
URL_FARM = getenv('URL_FARM', 'http://localhost:6000/dados')
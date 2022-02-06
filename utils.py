import mongoengine as db
from api_constants import mongo_password

database_name = "models"
password = mongo_password
DB_URI = "mongodb+srv://models:{}@models.dtdpx.mongodb.net/{}?retryWrites=true&w=majority".format(password, database_name)
db.connect(host=DB_URI)

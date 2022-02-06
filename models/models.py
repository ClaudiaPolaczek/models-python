from mongoengine import *
import datetime

class Model(Document):
   model_id = fields.IntField()
   eyes_color = fields.StringField()
   hair_color = fields.StringField()
   survey_id = fields.IntField()
   user_username = fields.StringField()

class User(Document):
   username = fields.StringField()
   avg_rate = fields.FloatField()
   main_photo_utl = fields.StringField()
   password = fields.StringField()
   role = fields.IntField()

class Notification(Document):
   notification_id = fields.IntField()
   added_date = fields.DateTimeField()
   content = fields.StringField()
   read_value = fields.IntField()
   user_username = fields.StringField()

class Survey(Document):
   survey_id = fields.IntField()
   birthday_year = fields.IntField()
   city = fields.StringField()
   first_name = fields.StringField()
   last_name = fields.StringField()
   gender = fields.StringField()
   instagram_name = fields.StringField()
   phone_number = fields.StringField()
   region = fields.StringField()
   regulations_agreement = fields.IntField()

class Photographer(Document):
   photographer_id = fields.IntField()
   survey_id = fields.IntField()
   user_username = fields.StringField()

class Comment(Document):
   comment_id = fields.IntField()
   added_date = fields.DateTimeField()
   content = fields.StringField()
   rated_user_username = fields.StringField()
   rating_user_username = fields.StringField()

class Photoshoot(Document):
   photoshoot_id = fields.IntField()
   city = fields.StringField()
   street = fields.StringField()
   duration = fields.IntField()
   house_number = fields.StringField()
   meeting_date = fields.DateTimeField()
   notes = fields.StringField()
   photoshoot_status = fields.IntField()
   topic = fields.StringField()
   invited_user_username = fields.StringField()
   inviting_user_username = fields.StringField()

class Portfolio(Document):
   portfolio_id = fields.IntField()
   added_date = fields.DateTimeField()
   description = fields.StringField()
   main_photo_url = fields.StringField()
   name = fields.StringField()
   user_username = fields.StringField()

class Image(Document):
   image_id = fields.IntField()
   added_date = fields.DateTimeField()
   file_url = fields.StringField()
   name = fields.StringField()
   portfolio_id = fields.IntField()

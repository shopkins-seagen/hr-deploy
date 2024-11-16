

from models import db,Employee,Review,upload_employees

db.connect()
db.drop_tables([Employee,Review])
db.create_tables([Employee,Review])
upload_employees('static/uploads/MOCK_DATA_3.csv')



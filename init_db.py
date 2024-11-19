from datetime import timedelta, date
from random import sample,randint,randrange
import math
from fake import Faker

from models import db,Employee,Review,upload_employees,get_employees,review_employee

def make_db():
    db.connect()
    db.drop_tables([Employee,Review])
    db.create_tables([Employee,Review])
    upload_employees('static/uploads/MOCK_DATA_3.csv')

def layoff():
    fake = Faker()
    emps = get_employees()
    ids = sample(range(1,len(emps)),int(math.floor(len(emps)/3)))
    for id in ids:
        e = emps[id]
        day = (date.today() - e.started).days
        ended = fake.date(start_date=f"-{day}d", end_date='today')
        e.ended = ended
        e.save()
    for e in emps:

        day = (date.today() - e.started).days
        for i in range(randint(1,3)):
            r = Review(employee_id=e.id,
                       review_date=fake.date(start_date=f"-{day}d", end_date='today'),
                       rating=randint(1,10),
                       comment="Automated Review")
            r.save()



make_db()
layoff()

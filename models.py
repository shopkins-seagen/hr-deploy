import os

from dominate.svg import desc
from peewee import Model, CharField, IntegerField, ForeignKeyField, DateField, JOIN,fn
from playhouse.db_url import connect
import csv
from datetime import datetime
import json



db = connect(os.environ.get('DATABASE_URL', 'sqlite:///hr.db'))
class Employee(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    address=CharField(null=True)
    ssn=CharField(null=True)
    dob = DateField()
    title=CharField()
    started=DateField()
    ended=DateField(null=True)

    class Meta:
        database = db
        db_table = 'Employee'
class Review(Model):
    id = IntegerField(primary_key=True)
    rating = IntegerField()
    review_date = DateField()
    comment=CharField()
    employee_id=ForeignKeyField(Employee,backref='Reviews')
    class Meta:
        database = db
        db_table = 'Reviews'

def get_employees():
   return (Employee.select(Employee,fn.Max(Review.review_date).alias("last_review"))
               .join(Review,JOIN.LEFT_OUTER)
               .group_by(Employee)
               .order_by(Employee.name))

def get_employee(id):
    e = (Employee.select(Employee, fn.Max(Review.review_date).alias("last_review"))
            .join(Review, JOIN.LEFT_OUTER)
            .where(Employee.id == id)
            .group_by(Employee))
    if len(e)>0:
        return e[0]
    return None

def add_employee(emp):
    try:
        employee = Employee.create(name=emp["name"],
                                   dob=emp["dob"],
                                   address=emp["address"],
                                   ssn=emp["ssn"],
                                   title=emp["title"],
                                   started=emp["started"])
        employee.save()
        return True,employee
    except Exception as ex:
        return False, repr(ex)

def delete_employee(id):
    try:
        e =Employee.get_by_id(id)
        return True,e.delete_instance()
    except Exception as ex:
        return False,repr(ex)
def update_employee(emp):

    try:
        e = Employee.get_by_id(int(emp["id"]))

        e.name = emp["name"]
        e.dob = emp["dob"]
        e.address=emp["address"]
        e.ssn = emp["ssn"]
        e.title=emp["title"]
        e.started =emp["started"]
        e.ended = emp["ended"]
        e.save()

        return True,e
    except Exception as ex:
        return False,repr(ex)

def review_employee(review):
    r = Review(employee_id=review["employee_id"],
               review_date=review["review_date"],
               rating=review["rating"],
               comment=review["comment"])
    r.save()

def  upload_employees(fn):
    with open(fn, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',',)
        next(reader,None)
        with db.atomic():
            for row in reader:
                Employee.create(name=row[0],address=row[1],ssn=row[2],dob=row[3],title=row[4],started=row[5],ended=row[6])

def generate_report(typ,fn):
    data = []

    if int(typ)==1:
        data=get_employees()
    elif int(typ)==2:
        data = [x for x in get_employees() if x.ended]
    elif int(typ)==3:
        raw = [x for x in get_employees() if x.last_review]
        data = [x for x in raw if (datetime.now().date() - x.last_review).days > 30]

    with open(fn,"w",newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["name","address","ssn","dob","title","started","ended","last_review"])
        for e in data:
            writer.writerow([e.name,e.address,e.ssn,e.dob,e.title,e.started,e.ended,e.last_review])

def get_reviews(id):
    return (Review().select().where(Review.employee_id==id).order_by(Review.review_date.desc()))




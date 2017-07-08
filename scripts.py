from flask_sqlalchemy import Pagination
from sqlalchemy import func, desc
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import aliased

from extensions import db, session
from models import Order, Person, Project, ProjectUser


def populate():
    p1 = Person('Alice')
    p2 = Person('Anamika')
    p3 = Person('Annie')
    p4 = Person('Anson')
    p5 = Person('Bob')
    p6 = Person('Carol')
    p7 = Person('Don')
    p8 = Person('Evi')

    session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])

    orders = [
        (p1, 'veggies', 120), (p2, 'veggies', 20), (p3, 'veggies', 120),
        (p4, 'veggies', 10), (p5, 'veggies', 280),
        (p1, 'ketchup', 80), (p1, 'spices', 220), (p1, 'tissues', 50), (p1, 'notebooks', 90),
        (p5, 'ketchup', 80)
    ]
    for person, name, price in orders:
        order = Order(person, name, price)
        session.add(order)

    p1 = Project('BSNL billing', 'alice')
    p2 = Project('BSNL payroll', 'bob')
    p3 = Project('ABC Institute', 'bob')

    pu1 = ProjectUser(p1, 'alice')
    pu2 = ProjectUser(p1, 'carol')
    pu3 = ProjectUser(p1, 'don')
    pu4 = ProjectUser(p2, 'alice')
    pu5 = ProjectUser(p2, 'carol')
    pu6 = ProjectUser(p3, 'don')
    pu7 = ProjectUser(p3, 'carol')

    session.add_all([p1, p2, p3, pu1, pu2, pu3, pu4, pu5, pu6, pu7])

    session.commit()


def print_generated_query(label, query):
    print '\n--------' + label + '--------'
    print str(query.statement.compile(dialect=postgresql.dialect()))
    print '--------'


def query():
    print 'query script'

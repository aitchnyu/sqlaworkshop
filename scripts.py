from flask_sqlalchemy import Pagination
from sqlalchemy import func, desc
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import aliased

from extensions import db, session
from models import Order, Person, Project, ProjectUser


def meow():
    print('meow')


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
    person_query = session.query(Person)
    print_generated_query('person', person_query)
    for person in person_query:
        print(person)

    person_order_query = session.query(Person, Order).filter(Order.person_id == Person.id)
    person_order_query = session.query(Person, Order).join(Order).order_by(Order.price)
    person_order_query = session.query(Person, Order)\
        .join(Order)\
        .distinct(Person.id)\
        .from_self()\
        .order_by(Order.price)
    print_generated_query('person and order', person_order_query)
    for person, order in person_order_query:
        print person, order

    sum = func.sum(Order.price)
    count = func.count()
    order_names_and_aggs = session\
        .query(Order.name, sum, count)\
        .filter(Order.price >= 15)\
        .group_by(Order.name)\
        .order_by(sum.desc())\
        .having(count > 1)
    print_generated_query('name, price and count', order_names_and_aggs)
    for name, sum, count in order_names_and_aggs:
        print(name, sum, count)

    sum = func.sum(Order.price)
    person_total = session.query(Person, sum)\
        .join(Order)\
        .group_by(Person.id)\
        .order_by(sum.desc())

    print_generated_query('person and total', person_total)
    for person, total in person_total:
        print(person, total)

    projects_alice_can_access = session.query(Project)\
        .outerjoin(ProjectUser)\
        .filter((ProjectUser.username == 'alice') | (Project.admin_username == 'alice'))
    print_generated_query('alice can access', projects_alice_can_access)
    for project in projects_alice_can_access:
        print(project)

    # both don and carol
    project_user_1 = aliased(ProjectUser, name='project_user_ek')
    project_user_2 = aliased(ProjectUser, name='project_user_do')
    projects_don_carol = session.query(Project)\
        .outerjoin(project_user_1, project_user_1.project_id == Project.id)\
        .outerjoin(project_user_2, project_user_2.project_id == Project.id)\
        .filter(project_user_1.username == 'carol')\
        .filter(project_user_2.username == 'don')
    print_generated_query('don and carol', projects_don_carol)
    for project in projects_don_carol:
        print(project)

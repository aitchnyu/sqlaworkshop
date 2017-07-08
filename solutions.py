# views
def orders():
    page = int(request.args.get('page', 1))
    paginator = Order.query.join(Person).add_entity(Person).paginate(page, 5)
    out_orders = []
    for order, person in paginator.items:
        out_orders.append({
            'person': person.name,
            'item': order.name,
            'price': order.price
        })
    return jsonify({
        'page': page,
        'pages': paginator.pages,
        'orders': out_orders
    })


# scripts
def query():
    person_query = session.query(Person)
    print_generated_query('person', person_query)
    for person in person_query:
        print(person)

    person_order_query = session.query(Person, Order).filter(Order.person_id == Person.id)
    person_order_query = session.query(Person, Order).join(Order).order_by(Order.price)
    person_order_query = session.query(Person, Order) \
        .join(Order) \
        .distinct(Person.id) \
        .from_self() \
        .order_by(Order.price)
    print_generated_query('person and order', person_order_query)
    for person, order in person_order_query:
        print person, order

    sum = func.sum(Order.price)
    count = func.count()
    order_names_and_aggs = session \
        .query(Order.name, sum, count) \
        .filter(Order.price >= 15) \
        .group_by(Order.name) \
        .order_by(sum.desc()) \
        .having(count > 1)
    print_generated_query('name, price and count', order_names_and_aggs)
    for name, sum, count in order_names_and_aggs:
        print(name, sum, count)

    sum = func.sum(Order.price)
    person_total = session.query(Person, sum) \
        .join(Order) \
        .group_by(Person.id) \
        .order_by(sum.desc())

    print_generated_query('person and total', person_total)
    for person, total in person_total:
        print(person, total)

    projects_alice_can_access = session.query(Project) \
        .outerjoin(ProjectUser) \
        .filter((ProjectUser.username == 'alice') | (Project.admin_username == 'alice'))
    print_generated_query('alice can access', projects_alice_can_access)
    for project in projects_alice_can_access:
        print(project)

    # both don and carol
    project_user_1 = aliased(ProjectUser, name='project_user_ek')
    project_user_2 = aliased(ProjectUser, name='project_user_do')
    projects_don_carol = session.query(Project) \
        .outerjoin(project_user_1, project_user_1.project_id == Project.id) \
        .outerjoin(project_user_2, project_user_2.project_id == Project.id) \
        .filter(project_user_1.username == 'carol') \
        .filter(project_user_2.username == 'don')
    print_generated_query('don and carol', projects_don_carol)
    for project in projects_don_carol:
        print(project)


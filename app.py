from flask import Flask
from extensions import db, migrate
from scripts import populate, query
from views import orders


def create_app():
    app = Flask(__name__)
    app.config.update({
        'DEBUG': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost/sqlaworkshop'})
    db.init_app(app)
    migrate.init_app(app, db)
    app.add_url_rule('/orders', view_func=orders, methods=['get'])
    app.cli.command()(populate)
    app.cli.command()(query)
    return app

app = create_app()

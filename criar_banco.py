from notpinterest import database, app
from notpinterest.models import Usuario, Foto

with app.app_context():
    database.create_all()
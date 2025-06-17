from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    users = [
        {'username': 'testuser', 'password': 'testpassword'},
        {'username': 'testtestuser', 'password': 'testtestpassword'}
    ]

    for user_data in users:
        username = user_data['username']
        password = user_data['password']
        user = User.query.filter_by(username=username).first()
        if user:
            print(f"Updating password for user {username}")
            user.set_password(password)
        else:
            print(f"Creating user {username}")
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
        db.session.commit()
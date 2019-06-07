from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Debate, Chat
from flask_socketio import SocketIO
import eventlet
from eventlet import wsgi


# Creating app instance
app = create_app('development')
socketio = SocketIO(app)
manager = Manager(app)

# socketio = SocketIO(app)
manager.add_command('server', Server)


migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@socketio.on('my event')
def handle_my_custom_event(json):
   chat = Chat(chat= str(json.get('msg')))
   db.session.add(chat)
   db.session.commit()


   socketio.emit('my response', json)
   

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User,  Debate=Debate, Chat=Chat)


if __name__ == "__main__":
    socketio.run(app, debug = True, port=4500)


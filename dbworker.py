from vedis import Vedis

db_file = "database.vdb"

def get_current_state(user_id):
    with Vedis(db_file) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return 0


def delete(user_id):
    with Vedis(db_file) as db:
        try:
            del db[user_id]
            return 1
        except KeyError:
            return 0


def set_state(user_id, value):
    with Vedis(db_file) as db:
        try:
            db[user_id] = value
            return True
        except:
            return
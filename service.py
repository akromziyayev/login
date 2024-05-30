from db import cur, conn
from models import User
from session import Session
import utils

login_try_count = 0


session = Session()


def login(username:str, password:str):
    global login_try_count
    user: Session | None = session.check_session()
    if user:
        return utils.BadRequest('You already logged in', status_code=401)

    get_user_by_username = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username, username)
    user_data = cur.fetchone()
    if not user_data:
        return utils.BadRequest('Username not found in my DB')
    _user = User(username=user_data[1], password=user_data[2], role=user_data[3], status=user_data[4],
                 login_try_count=user_data[5])

    if password != _user.password:
        if login_try_count == 3:
            print("limit tugadi")
            quit()
        login_try_count += 1
        update_count_query = """update users set login_try_count = login_try_count + 1 where username = %s;"""
        cur.execute(update_count_query, (_user.username,))
        conn.commit()

    user.add_session(_user)
    return utils.ResponseData('User Successfully Logged in')


while True:
    choice = input('Enter your choice: ')
    if choice == '1':
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        login(username, password)
    else:
        break

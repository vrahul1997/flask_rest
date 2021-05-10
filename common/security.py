# ##
# ##
# ##
# ##      not needed if flask_JWT_extended is used
# ##
# ##
# ##
# ##

from resources.user import UserModel
from flask import request, jsonify
from functools import wraps


def authenticate(username, password):
    user = UserModel.find_by_username(username)  # add None as default value
    if user and user.password == password:
        print(vars(user))
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)


def jwt_is_required(realm=None):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if request.headers.get("Authorization") is not None:
                return f(*args, **kwargs)
            else:
                return jsonify({"message": "JWT not present"})

        return decorator

    return wrapper


# sample decorator function
"""
auth = True
numbers = [i for i in range(30)]


def is_auth(func):
    def wrapper(num_list):
        if not auth:
            print("access denied")
        else:
            print("authenticated")
            res = func(num_list)
            print(res)
            print("executed")

    return wrapper


@is_auth
def calulate(num_list):
    sum = 0
    for i in num_list:
        sum += i
    return sum

funtion
    wrapper(f)
    wraps(f)
        decor(args , kwars)

        return decor
    return wrapper


calulate(numbers)
"""
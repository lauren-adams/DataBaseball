from app.daos.user_dao import find_user, test
import app.util.encrypt as encrypt

def validate_signup(username, password, passwordConfirmation):
    """ Returns an error message (if needed) for the given signup info """

    # verify username is not taken
    if find_user(username) is not None:
        return "username already taken"

    # verify username is long enough
    if len(username) < 1:
        return "username too short"

    # verity both password match
    if password != passwordConfirmation: 
        return "passwords don't match"

    # verify password is long enough
    if len(password) < 1:
        return "password too short"


def validate_login(username, password):
    """ Returns an error message (if needed) for the given login info """

    user = find_user(username)

    # verify user exists
    if user is None:
        return "username/password don't match"

    # verify hashes match
    if user.hash != encrypt.sha1(password):
        return "username/password don't match"

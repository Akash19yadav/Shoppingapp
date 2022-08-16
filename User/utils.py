import re
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# This function is returning the hashed password
def hash_password(password: str):
    return pwd_context.hash(password)


# This function is verifying the plane password with the hashed password present into db
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# This is validation class which will be used throughout the project to verify the fields
class Validation:
    @staticmethod
    def name(name):
        if len(name) < 3:
            return True
        return False

    @staticmethod
    def phone_validation(number):
        if len(number) == 10:
            if "." not in number:
                return False
        return True

    @staticmethod
    def password_check(pswd1, pswd2):
        if pswd1 != pswd2:
            return True
        if len(pswd1) < 6:
            return True
        return False

    @staticmethod
    def email_validation(email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        process = re.compile(regex)
        flag = re.match(process, email)
        if flag:
            return False
        return True

    @staticmethod
    def postal_code(code: str):
        regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
        process = re.compile(regex)
        flag = re.match(process, code)
        if flag:
            return False
        return True


validation = Validation()

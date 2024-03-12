"""
Regex func
"""

import re

class Validator:
    """
    validor of regexes
    """
    def validate_name(self, name_surname: str):
        """
        validate name and surname
        """
        if re.search(r'^[A-Z][a-z]{2,30}$' ,name_surname):
            return True
        return False

    def validate_surname(self, name_surname: str):
        """
        validate name and surname
        """
        if re.search(r'^[A-Z][a-z]{2,30}$' ,name_surname):
            return True
        return False

    def validate_phone(self, phone: str):
        """
        validates phone
        """
        if re.search\
(r'\+[0-9]{1,2}[0-9]{10}$|^\+[0-9]{1,2} [(]0[0-9]{2}[)] [0-9]{3}-[0-9]{2}-[0-9]{2}$', phone):
            return True
        return False

    def validate_email(self, email: str):
        """
        validates email
        """
        if re.search(r"^[^.][a-z!#$%&'*+-/=?^_`{|}]{1,64}@[a-z.]{1,255}\.(com|org|edu|gov|net|ua)$",
         email):
            return True
        return False

    def validate_password(self, password: str):
        """
        validates password
        """
        if re.search('^[0-9a-z]',password):
            return True
        return False

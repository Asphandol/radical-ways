"""
validates users data
"""

import re
class Validator:
    """
    validator class
    """
    def validate_name(self, name_surname: str):
        """
        Validates name and surname.
        """
        pattern = r"^[A-Z][a-z]{2,30}$"
        return bool(re.match(pattern, name_surname))

    def validate_surname(self, name_surname: str):
        """
        Validates surname.
        """
        pattern = r"^[A-Z][a-z]{2,30}$"
        return bool(re.match(pattern, name_surname))

    def validate_phone(self, phone: str):
        """
        Validates phone.
        """
        for el in phone:
            if not el.isdigit() or el not in ('+', '-', ' '):
                return False
        return True

    def validate_email(self, email: str):
        """
        Validates email.
        """
        pattern = r"^[^\s@]+@[^\s@]+\.(com|org|edu|gov|net|ua)$"
        return bool(re.match(pattern, email))



    def validate_password(self, password: str):
        """
        Validates password.
        """
        return not (' ' in password)

class Validator:
    def validate_name(self, name_surname: str):
        """
        Validates name and surname.
        """
        if len(name_surname.split())!=1:
            return False

        name = name_surname.split()[0]

        for i in name:
            if i.isdigit():
                return False

        if len(name) > 31:
            return False
        return True

    def validate_surname(self, name_surname: str):
        """
        Validates surname.
        """
        if len(name_surname.split())!=2:
            return False

        surname = name_surname.split()[1]

        for i in surname:
            if i.isdigit():
                return False

        if len(surname) > 31:
            return False
        return True

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
        if '@' not in email or '.' not in email:
            return False
        
        if len(email.split('@'))!=2:
            return False
 
        if len(email.split('@')[1].split('.'))!=2:
            return False
        
        return True
        


    def validate_password(self, password: str):
        """
        Validates password.
        """
        if len(password)<8:
            return False
        if not any(el.isupper() for el in password):
            return False
        if not any(el.isdigit() for el in password):
            return False
        return False


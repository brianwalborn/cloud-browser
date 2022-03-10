from flask import flash

class Validator():
    def __init__(self):
        self.immune_fields = []
        self.invalid_fields = []

    def validate_required_fields(self, form):
        self.invalid_fields.clear()
        
        for item in form:
            if not form[item] and item not in self.immune_fields:
                flash(f'\'{item}\' is a required field', 'error')
                self.invalid_fields.append(item)

        valid = len(self.invalid_fields) == 0

        return valid

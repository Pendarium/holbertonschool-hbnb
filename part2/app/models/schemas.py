from marshmallow import Schema, fields, validate, validates, ValidationError


class UserSchema(Schema):
    """
    Schéma de validation pour les objets User.
    Utilisé pour valider les données avant création d'un utilisateur.
    """
    email = fields.Email(required=True, error_messages={
        "required": "Email is required"})
    password = fields.Str(required=True, validate=validate.Length(min=3))
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)

    @validates("password")
    def validate_password_strength(self, value):
        """
        Vérifie que le mot de passe contient à
        la fois des lettres et des chiffres.
        """
        if len(value) < 6:
            raise ValidationError(
                "Password must be at least 6 characters long.")
        if value.isalpha() or value.isdigit():
            raise ValidationError(
                "Password must include both letters and numbers.")

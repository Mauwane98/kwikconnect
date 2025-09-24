
from backend.models.user import User, UserRole
from backend.models.token_blocklist import TokenBlocklist
from backend.errors import ConflictError, UnauthorizedError
from flask_jwt_extended import create_access_token, create_refresh_token
import datetime

class AuthService:
    @staticmethod
    def register_user(data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role_str = data.get('role')

        if User.find_by_email(email):
            raise ConflictError("User with that email already exists")

        role = UserRole[role_str.upper()]

        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        new_user.save_to_db()

        additional_claims = {"role": new_user.role.value}
        access_token = create_access_token(identity=new_user.id, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=new_user.id, additional_claims=additional_claims)

        return new_user, access_token, refresh_token

    @staticmethod
    def login_user(data):
        email = data.get('email')
        password = data.get('password')

        user = User.find_by_email(email)
        if user and user.check_password(password):
            user.last_login = datetime.datetime.utcnow()
            user.save_to_db()

            additional_claims = {"role": user.role.value}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.id, additional_claims=additional_claims)
            return user, access_token, refresh_token
        else:
            raise UnauthorizedError("Invalid email or password")

    @staticmethod
    def logout_user(jti):
        blocklisted_token = TokenBlocklist(jti=jti)
        blocklisted_token.save_to_db()

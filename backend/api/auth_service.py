from backend.models.user import User
from backend.errors import ConflictError, UnauthorizedError
from flask_jwt_extended import create_access_token, create_refresh_token
import datetime
import requests

class AuthService:
    @staticmethod
    def login_with_google(access_token):
        try:
            # Verify the access token with Google
            response = requests.get(f"https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={access_token}")
            response.raise_for_status()  # Raise an exception for bad status codes
            google_user_info = response.json()

            email = google_user_info.get('email')
            if not email:
                raise UnauthorizedError("Email not provided by Google")

            # Check if user exists
            user = User.find_by_email(email)
            if not user:
                # Create a new user
                full_name = google_user_info.get('name', '')
                # Split full_name into first_name and last_name
                first_name = full_name.split(' ')[0]
                last_name = ' '.join(full_name.split(' ')[1:])
                user = User.create_user(
                    email=email,
                    password=None,  # No password for Google login
                    full_name=full_name,
                    role='customer'
                )

            additional_claims = {"role": user.get('role')}
            access_token = create_access_token(identity=str(user.get('_id')), additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=str(user.get('_id')), additional_claims=additional_claims)

            return User.to_dict(user), access_token, refresh_token

        except requests.exceptions.HTTPError as err:
            raise UnauthorizedError("Invalid Google access token")
        except Exception as err:
            raise UnauthorizedError(str(err))

    @staticmethod
    def register_user(data):
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        role = data.get('role', 'customer') # Default to customer if not provided

        if User.find_by_email(email):
            raise ConflictError("User with that email already exists")

        new_user = User(email=email, password=password, full_name=full_name, role=role)
        new_user.save()

        additional_claims = {"role": new_user.role}
        access_token = create_access_token(identity=str(new_user._id), additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=str(new_user._id), additional_claims=additional_claims)

        return new_user, access_token, refresh_token

    @staticmethod
    def login_user(data):
        email = data.get('email')
        password = data.get('password')
        user = User.find_by_email(email)
        # user is a dict (document) when using BaseModel; validate password hash accordingly
        if user:
            # password hash field is stored as 'password_hash'
            password_hash = user.get('password_hash') or user.get('password')
            if password_hash and User.check_password(password_hash, password):
                additional_claims = {"role": user.get('role')}
                access_token = create_access_token(identity=str(user.get('_id') or user.get('_id')), additional_claims=additional_claims)
                refresh_token = create_refresh_token(identity=str(user.get('_id') or user.get('_id')), additional_claims=additional_claims)
                # return a frontend-friendly user dict
                return User.to_dict(user), access_token, refresh_token

        raise UnauthorizedError("Invalid email or password")

    # @staticmethod
    # def logout_user(jti):
    #     # Token blocklisting needs to be re-implemented for MongoDB
    #     pass
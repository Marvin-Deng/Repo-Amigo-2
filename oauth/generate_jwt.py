import time
from jwt import JWT, jwk_from_pem

from constants import PEM_PATH, CLIENT_ID


def generate_jwt() -> str:
    """
    Generates a JWT using a private PEM file and an app ID.

    Returns:
        str: The encoded JWT.
    """
    # Load the private key from the PEM file
    with open(PEM_PATH, "rb") as pem_file:
        signing_key = jwk_from_pem(pem_file.read())

    # Define the JWT payload
    payload = {"iat": int(time.time()), "exp": int(time.time()) + 600, "iss": CLIENT_ID}

    jwt_instance = JWT()
    encoded_jwt = jwt_instance.encode(payload, signing_key, alg="RS256")

    return encoded_jwt


if __name__ == "__main__":
    # Generate JWT using constants
    jwt_token = generate_jwt()
    print(f"JWT: {jwt_token}")

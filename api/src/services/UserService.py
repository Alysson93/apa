from src.repositories.UserRepository import UserRepository

class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository
    
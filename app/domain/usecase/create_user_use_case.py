from app.infrastructure.adapter.create_user_adapter import CreateUserAdapter


class CreateUserUseCase:

    def __init__(self):
        self.create_user_adapter = CreateUserAdapter()

    async def create_user(self, username, password):
        user = await self.find_by_name(username)
        if user:
            raise FileExistsError
        return await self.create_user_adapter.create_user(username, password)

    async def check_user(self, username, password):
        return await self.create_user_adapter.check_user(username, password)

    async def find_by_name(self, username):
        return await self.create_user_adapter.find_by_username(username)

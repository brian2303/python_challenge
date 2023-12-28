from graphene import ObjectType, String


class SaveBookResponse(ObjectType):
    id = String()
    message = String()

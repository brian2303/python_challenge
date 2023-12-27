from graphene import ObjectType, String, List


class Book(ObjectType):
    id = String()
    resource = String()

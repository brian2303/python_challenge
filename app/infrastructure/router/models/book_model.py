from graphene import ObjectType, String, List


class Book(ObjectType):
    id = String()
    resource = String()
    title = String()
    subtitle = String()
    categories = List(String)

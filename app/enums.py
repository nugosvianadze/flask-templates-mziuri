from enum import Enum


class CustomEnum(Enum):
    @classmethod
    def choices(cls):
        return [role for role in cls]


class RoleEnum(CustomEnum):
    USER = 'User'
    ADMIN = 'Admin'
    EDITOR = 'Editor'


class FoodEnum(CustomEnum):
    VEGETARIAN = 'Vegetarian'


class StatusEnum(CustomEnum):
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'


# print(RoleEnum.EDITOR, RoleEnum.EDITOR.value, RoleEnum.EDITOR.name)
print(FoodEnum.choices())
print(RoleEnum.choices())
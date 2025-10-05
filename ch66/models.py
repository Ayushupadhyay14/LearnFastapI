from sqlmodel import Field, SQLModel

class UserAddressLink(SQLModel, table=True):
  user_id : int = Field(foreign_key="user.id", primary_key=True)
  address_id : int = Field(foreign_key="address.id", primary_key=True)

class User(SQLModel, table=True):
  id: int = Field(primary_key=True)
  name: str
  email: str

# One to One
class Profile(SQLModel, table=True):
  id: int = Field(primary_key=True)
  user_id : int = Field(foreign_key="user.id", unique=True)
  bio: str

# One to Many
class Post(SQLModel, table=True):
   id: int = Field(primary_key=True)
   user_id : int = Field(foreign_key="user.id")
   title: str
   content: str

# Many to Many
class Address(SQLModel, table=True):
  id: int = Field(primary_key=True)
  street: str
  city: str
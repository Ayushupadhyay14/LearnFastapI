from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Table, Column, Integer
from db import engine

class Base(DeclarativeBase):
  pass

# User Model
class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(50), nullable=False)
  email: Mapped[str] = mapped_column(String, nullable=False, unique=True)

  # One-to-Many: User to Post
  posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", cascade="all, delete")
  
  # One-to-One: User to Profile
  profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete")
  
  # Many-to-Many: User to Address
  address: Mapped[list["Address"]] = relationship("Address", back_populates="user", cascade="all, delete")
  
  def __repr__(self) -> str:
    return f"<User(id={self.id}, name={self.name}, email={self.email})>"

# Post Model One-to-Many
class Post(Base):
  __tablename__ = "posts"

  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  title: Mapped[str] = mapped_column(String, nullable=False)
  content: Mapped[str] = mapped_column(String, nullable=False)

  user: Mapped["User"] = relationship("User", back_populates="posts")
  
  def __repr__(self) -> str:
    return f"<Post id={self.id} title={self.title}>"
  
# Profile Model (One-to-One)
class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    bio: Mapped[str] = mapped_column(String, nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="profile")
    
    def __repr__(self) -> str:
      return f"<Profile id={self.id} user_id={self.user_id}>"

# Address Model (Many-to-Many)
class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped[list["User"]] = relationship("User", back_populates="address")
    
    def __repr__(self) -> str:
      return f"<Address id={self.id} street={self.street} country={self.country}>"

user_address_association = Table(
    "user_address_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("address_id", Integer, ForeignKey("address.id", ondelete="CASCADE"), primary_key=True),
)

#  Create Table
def create_tables():
  Base.metadata.create_all(engine)

#  Drop Table
def drop_tables():
  Base.metadata.drop_all(engine)
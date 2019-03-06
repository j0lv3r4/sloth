"""Models"""

from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    DateTime,
    Table,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL


Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


user_likes = Table(
    "user_liking",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("note_id", Integer, ForeignKey("notes.id")),
)


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    avatar = Column(String)
    ap_id = Column(String, unique=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String)
    domain = Column(String)
    private_key = Column(String)
    public_key = Column(String)
    webfinger = Column(String)
    auth_token = Column(String)
    created_by = Column(DateTime, default=datetime.utcnow())
    updated_by = Column(DateTime, default=datetime.utcnow())
    notes = relationship("Note")
    liked = relationship("Note", secondary=user_likes, back_populates="likes")

    following = relationship(
        "User",
        lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        backref="followers",
    )

    def __repr__(self):
        return "<User {0}>".format(self)


user_following = Table(
    "user_following",
    Base.metadata,
    Column("user_id", Integer, ForeignKey(User.id), primary_key=True),
    Column("following_id", Integer, ForeignKey(User.id), primary_key=True),
)


class Note(Base):
    """Note model"""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    ap_id = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_by = Column(DateTime, default=datetime.utcnow())
    updated_by = Column(DateTime, default=datetime.utcnow())
    likes = relationship("User", secondary=user_likes, back_populates="liked")

    def __rep__(self):
        return "<Note {0}>".format(self)


Base.metadata.create_all(engine)

# テーブルをpythonで処理するために定義する感じ
# 変更したら以下のコマンドで更新
# crudsのみで呼び出される

import datetime
import uuid
import sys
from sqlalchemy import (Column, String, Text, ForeignKey,CHAR, VARCHAR, INT, Boolean,  \
                create_engine, MetaData, DECIMAL, DATETIME, exc, event, Index, \
                and_)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

sys.dont_write_bytecode = True

base = declarative_base()

class Followlist(base):
    __tablename__ = 'followlist'
    following = Column(String(36), ForeignKey("user.id"), primary_key=True)
    followed = Column(String(36), ForeignKey("user.id"), primary_key=True)
    flag = Column(Boolean, default=True)
    user_following = relationship("User", foreign_keys=[following], back_populates="following")
    user_followed = relationship("User", foreign_keys=[followed], back_populates="followed_by")


class Good(base):
    __tablename__ = 'good'
    user_id = Column(CHAR(36), ForeignKey("user.id"), primary_key=True)  # 型を一致させる
    post_id = Column(CHAR(36), ForeignKey("post.id"), primary_key=True)
    flag = Column(Boolean, default=True)
    user = relationship("User", back_populates="good")
    post = relationship("Post", back_populates="good")

class User(base):
    __tablename__ = 'user'
    id = Column(CHAR(36), primary_key=True)
    name = Column(VARCHAR(10))
    email = Column(VARCHAR(30))
    password = Column(VARCHAR(64))
    comment = Column(VARCHAR(100))
    image = Column(VARCHAR(255))
    good = relationship("Good", back_populates="user")
    post = relationship("Post", back_populates="user")
    report = relationship("Report", back_populates="user")
    following = relationship(
        "Followlist",
        foreign_keys="[Followlist.following]",
        back_populates="user_following",
        cascade="all, delete-orphan",
    )
    followed_by = relationship(
        "Followlist",
        foreign_keys="[Followlist.followed]",
        back_populates="user_followed",
        cascade="all, delete-orphan",
    )
    def __init__(self):
        self.id = str(uuid.uuid4())
        
        
class Post(base):
    __tablename__ = 'post'
    id = Column(CHAR(36), primary_key=True)
    title = Column(VARCHAR(17))
    caption = Column(VARCHAR(50))
    create_date_time = Column(DATETIME)
    goodcount = Column(INT, default=0)
    image = Column(VARCHAR(255))
    user_id = Column(CHAR(36), ForeignKey("user.id"))  # 型を一致させる
    user = relationship("User", back_populates="post")
    good = relationship('Good', back_populates='post', cascade='all, delete-orphan')

    def __init__(self):
        self.id = str(uuid.uuid4())
        now_data_time = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        self.create_date_time = now_data_time
       
 
class Report(base):
    __tablename__ = 'report'    
    id = Column(CHAR(36), primary_key=True)
    times = Column(INT, default=0)
    update_date_time = Column(DATETIME)
    user_id = Column(CHAR(36), ForeignKey("user.id"))
    user = relationship("User", back_populates="report")

    def __init__(self):
        self.id = str(uuid.uuid4())
        now_data_time = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        self.update_date_time = now_data_time
        

class Admin(base):
    __tablename__ = 'admin'
    id = Column(CHAR(36), primary_key=True)
    name = Column(VARCHAR(10))
    email = Column(VARCHAR(30))
    password = Column(VARCHAR(64))

    def __init__(self):
        self.id = str(uuid.uuid4())
        
        
class CorpInfo(base):
    __tablename__ = 'corpinfo'
    id = Column(CHAR(36), primary_key=True)
    corpname = Column(VARCHAR(30))
    email = Column(VARCHAR(30))
    manager = Column(VARCHAR(30))
    # url = Column(VARCHAR(128))
    image = Column(VARCHAR(255))

    def __init__(self):
        self.id = str(uuid.uuid4())

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

Base = declarative_base()


class Datasets(Base):
    __tablename__ = 'datasets'
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()'))    
    name = Column(String)
    filename = Column(String)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    datasetsid = Column(postgresql.UUID(as_uuid=True), ForeignKey('datasets.id'))    
    firstname = Column(String)
    lastname = Column(String)
    dateofbirth = Column(String)
    gender = Column(Integer)
    email = Column(postgresql.ARRAY(Text), nullable=True)
    phone = Column(postgresql.ARRAY(Text), nullable=True)
    maritalstatus = Column(Integer)
    income = Column(Integer)
    
    credentials = relationship("Credentials", backref="profile", uselist=False)
    contacts = relationship("Contacts", backref="profile", uselist=False)
    place_of_residence = relationship("PlaceOfResidence", backref="profile", uselist=False)
    personal_interests = relationship("PersonalInterests", backref="profile", uselist=False)
    device_information = relationship("DeviceInformation", backref="profile", uselist=False)
    cookies = relationship("Cookies", backref="profile", uselist=False)
    settings = relationship("Settings", backref="profile", uselist=False)
    work_and_education = relationship("WorkAndEducation", backref="profile", uselist=False)
    basic_data = relationship("BasicData", backref="profile", uselist=False)



class Credentials(Base):
    __tablename__ = 'credentials'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    emails = Column(Text)
    phones = Column(Text)


class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    mobilephone = Column(String)
    address = Column(String)
    linkedaccounts = Column(postgresql.ARRAY(Text), nullable=True)
    website = Column(String)


class PlaceOfResidence(Base):
    __tablename__ = 'placeofresidence'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    currentcity = Column(String)
    birthplace = Column(String)
    othercities = Column(postgresql.ARRAY(Text), nullable=True)


class PersonalInterests(Base):
    __tablename__ = 'personalinterests'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    briefdescription = Column(Text)
    hobby = Column(postgresql.ARRAY(Text), nullable=True)
    sport = Column(postgresql.ARRAY(Text), nullable=True)   


class DeviceInformation(Base):
    __tablename__ = 'deviceinformation'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    operatingsystem = Column(String)
    displayresolution = Column(String)
    browser = Column(String)
    isp = Column(String)
    adblock = Column(Boolean)


class Cookies(Base):
    __tablename__ = 'cookies'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    sessionstate = Column(Text)
    language = Column(String)
    region = Column(String)
    recentpages = Column(postgresql.ARRAY(Text), nullable=True)
    productid = Column(Integer)
    productname = Column(String)
    productprice = Column(Integer)
    quantity = Column(Integer)
    subtotal = Column(Integer)
    total = Column(Integer)
    couponcode = Column(String)
    shippinginformation = Column(Text)
    taxinformation = Column(Text)


class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    email = Column(postgresql.ARRAY(Text), nullable=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    profileids = Column(postgresql.ARRAY(Integer), nullable=True)
    basicdataids = Column(postgresql.ARRAY(Integer), nullable=True)
    contactsids = Column(postgresql.ARRAY(Integer), nullable=True)
    workandeducationids = Column(postgresql.ARRAY(Integer), nullable=True)
    placeofresidenceids = Column(postgresql.ARRAY(Integer), nullable=True)
    personalinterestsids = Column(postgresql.ARRAY(Integer), nullable=True)


class WorkAndEducation(Base):
    __tablename__ = 'workandeducation'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    placeofwork = Column(String)
    skills = Column(postgresql.ARRAY(Text), nullable=True)
    university = Column(String)
    faculty = Column(String)


class BasicData(Base):
    __tablename__ = 'basicdata'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    interests = Column(postgresql.ARRAY(Text), nullable=True)
    languages = Column(postgresql.ARRAY(Text), nullable=True)
    religionviews = Column(postgresql.ARRAY(Text), nullable=True)
    politicalviews = Column(postgresql.ARRAY(Text), nullable=True)


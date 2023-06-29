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
    gender = Column(String)
    email = Column(postgresql.ARRAY(String), nullable=True)
    phone = Column(postgresql.ARRAY(String), nullable=True)
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
    linkedaccounts = Column(postgresql.ARRAY(String), nullable=True)
    website = Column(String)


class PlaceOfResidence(Base):
    __tablename__ = 'placeofresidence'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    currentcity = Column(String)
    birthplace = Column(String)
    othercities = Column(postgresql.ARRAY(String), nullable=True)


class PersonalInterests(Base):
    __tablename__ = 'personalinterests'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    briefdescription = Column(Text)
    hobby = Column(String)
    sport = Column(String)


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
    recentpages = Column(postgresql.ARRAY(String), nullable=True)
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
    email = Column(String)
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
    skills = Column(postgresql.ARRAY(String), nullable=True)
    university = Column(String)
    faculty = Column(String)


class BasicData(Base):
    __tablename__ = 'basicdata'
    id = Column(Integer, primary_key=True)
    profileid = Column(Integer, ForeignKey('profile.id'))
    interests = Column(Text)
    languages = Column(postgresql.ARRAY(String), nullable=True)
    religionviews = Column(String)
    politicalviews = Column(String)


# def upgrade():
#     op.create_table(
#         'datasets',
#         sa.Column('id', sa.UUID(), nullable=False),
#         sa.Column('name', sa.String(), nullable=True),
#         sa.Column('filename', sa.String(), nullable=True),
#         sa.PrimaryKeyConstraint('id')
#     )

#     op.create_table(
#         'profile',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('datasetsid', sa.UUID(), nullable=False),
#         sa.Column('firstname', sa.String(), nullable=True),
#         sa.Column('lastname', sa.String(), nullable=True),
#         sa.Column('dateofbirth', sa.String(), nullable=True),
#         sa.Column('gender', sa.String(), nullable=True),
#         sa.Column('email', postgresql.ARRAY(sa.String()), nullable=True),
#         sa.Column('phone', postgresql.ARRAY(sa.String()), nullable=True),
#         sa.Column('maritalstatus', sa.Integer(), nullable=True),
#         sa.Column('income', sa.Integer(), nullable=True),
#         sa.PrimaryKeyConstraint('id', 'datasetsid'),
#     )
#     op.create_index('idx_profile_id', 'profile', ['id'], unique=True)

#     op.create_table(
#         'credentials',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('profileid', sa.Integer(), nullable=True),
#         sa.Column('emails', sa.Text(), nullable=True),
#         sa.Column('phones', sa.Text(), nullable=True),
#         sa.ForeignKeyConstraint(['profileid'], ['profile.id']),
#         sa.PrimaryKeyConstraint('id')
#     )

#     op.create_table(
#         'contacts',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('profileid', sa.Integer(), nullable=True),
#         sa.Column('mobilephone', sa.String(), nullable=True),
#         sa.Column('address', sa.String(), nullable=True),
#         sa.Column('linkedaccounts', postgresql.ARRAY(sa.String()), nullable=True),
#         sa.Column('website', sa.String(), nullable=True),
#         sa.ForeignKeyConstraint(['profileid'], ['profile.id']),
#         sa.PrimaryKeyConstraint('id')
#     )

#     op.create_table(
#         'placeofresidence',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('profileid', sa.Integer(), nullable=True),
#         sa.Column('currentcity', sa.String(), nullable=True),
#         sa.Column('birthplace', sa.String(), nullable=True),
#         sa.Column('othercities', postgresql.ARRAY(sa.String()), nullable=True),
#         sa.ForeignKeyConstraint(['profileid'], ['profile.id']),
#         sa.PrimaryKeyConstraint('id')
#     )

#     op.create_table(
#         'personalinterests',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('profileid', sa.Integer(), nullable=True),
#         sa.Column('briefdescription', sa.Text(), nullable=True),
#         sa.Column('hobby', sa.String(), nullable=True),
#         sa.Column('sport', sa.String(), nullable=True),
#         sa.ForeignKeyConstraint(['profileid'], ['profile.id']),
#         sa.PrimaryKeyConstraint('id')
#     )

#     op.create_table(
#         'deviceinformation',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('profileid', sa.Integer(), nullable=True),
#         sa.Column('operatingsystem', sa.String(), nullable=True),
#         sa.Column('displayresolution', sa.String(), nullable=True),
#         sa.Column('browser', sa.String(), nullable=True),
#         sa.Column('isp', sa.String(), nullable=True),
#         sa.Column('adblock', sa.Boolean(), nullable=True),
#         sa.ForeignKeyConstraint(['profileid'], ['profile.id']),
#         sa.PrimaryKeyConstraint('id')
#     )

#     op.create_table(
#         'cookies',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('profileid', sa.Integer(), nullable=True),
#         sa.Column('sessionstate', sa.Text(), nullable=True),
#         sa.Column('language', sa.String(), nullable=True),
#         sa.Column('region', sa.String(), nullable=True),
#         sa.Column('recentpages', postgresql.ARRAY(sa.String()), nullable=True),
#         sa.Column('productid', sa.Integer(), nullable=True),
#         sa.Column('productname', sa.String(), nullable=True),
#         sa.Column('productprice', sa.Integer(), nullable=True),
#         sa.Column('quantity', sa.Integer(), nullable=True),
#         sa.Column('subTotal', sa.Integer(), nullable=True),
#         sa.Column('total', sa.Integer(), nullable=True),
#         sa.Column('couponcode', sa.String(), nullable=True),
#         sa.Column('shippingiinformation', sa.Text(), nullable=True),
#         sa.Column('taxinformation', sa.Text(), nullable=True),
#         sa.ForeignKeyConstraint(['profileid'], ['profile.id']),
#         sa.PrimaryKeyConstraint('id')
#     )

#     op.create_table(
#         'settings',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('email', sa.String(), nullable=True),
#         sa.Column('profileid', sa.Integer(), nullable=True),
#         sa.Column('profileids', postgresql.ARRAY(sa.Integer()), nullable=True),
#         sa.Column('basicdataids', postgresql.ARRAY(sa.Integer()), nullable=True),
#         sa.Column('contactsids', postgresql.ARRAY(sa.Integer()), nullable=True),
#         sa.Column('workandeducationids', postgresql.ARRAY(sa.Integer()), nullable=True),
#         sa.Column('placeofresidenceids', postgresql.ARRAY(sa.Integer()), nullable=True),
#         sa.Column('personalinterestsids', postgresql.ARRAY(sa.Integer()), nullable=True),
#         sa.ForeignKeyConstraint(['profileid'], ['profile.id']),
#         sa.PrimaryKeyConstraint('id')
#     )

#     op.create_table(
#         'workandeducation',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('profileid', sa.Integer(), nullable=True),
#         sa.Column('placeofwork', sa.String(), nullable=True),
#         sa.Column('skills', postgresql.ARRAY(sa.String()), nullable=True),
#         sa.Column('university', sa.String(), nullable=True),
#         sa.Column('faculty', sa.String(), nullable=True),
#         sa.ForeignKeyConstraint(['profileid'], ['profile.id']),
#         sa.PrimaryKeyConstraint('id')
#     )

#     op.create_table(
#         'basicdata',
#         sa.Column('id', sa.Integer(), nullable=False),
#         sa.Column('profileid', sa.Integer(), nullable=True),
#         sa.Column('interests', sa.Text(), nullable=True),
#         sa.Column('languages', postgresql.ARRAY(sa.String()), nullable=True),
#         sa.Column('religionviews', sa.String(), nullable=True),
#         sa.Column('politicalviews', sa.String(), nullable=True),
#         sa.ForeignKeyConstraint(['profileid'], ['profile.id']),
#         sa.PrimaryKeyConstraint('id')
#     )




# def downgrade():
#     op.drop_table('datasets')
#     op.drop_table('profile')
#     op.drop_table('credentials')
#     op.drop_table('contacts')
#     op.drop_table('placeofresidence')
#     op.drop_table('personalinterests')
#     op.drop_table('deviceinformation')
#     op.drop_table('cookies')
#     op.drop_table('settings')
#     op.drop_table('workandeducation')
#     op.drop_table('basicdata')
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

Base = declarative_base()


class Datasets(Base):
    __tablename__ = 'datasets'
    id = Column(String, primary_key=True)
    name = Column(String)
    filename = Column(String)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    datasetsId = Column(String, ForeignKey('datasets.id'))
    firstName = Column(String)
    lastName = Column(String)
    dateOfBirth = Column(String)
    gender = Column(String)
    email = Column(Text)
    phone = Column(Text)
    maritalStatus = Column(Integer)
    income = Column(Integer)


class Credentials(Base):
    __tablename__ = 'credentials'
    id = Column(Integer, primary_key=True)
    profileId = Column(Integer, ForeignKey('profile.id'))
    emails = Column(Text)
    phones = Column(Text)


class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    profileId = Column(Integer, ForeignKey('profile.id'))
    mobilePhone = Column(String)
    address = Column(String)
    linkedAccounts = Column(Text)
    website = Column(String)


class PlaceOfResidence(Base):
    __tablename__ = 'placeOfResidence'
    id = Column(Integer, primary_key=True)
    profileId = Column(Integer, ForeignKey('profile.id'))
    currentCity = Column(String)
    birthPlace = Column(String)
    otherCities = Column(Text)


class PersonalInterests(Base):
    __tablename__ = 'personalInterests'
    id = Column(Integer, primary_key=True)
    profileId = Column(Integer, ForeignKey('profile.id'))
    briefDescription = Column(Text)
    hobby = Column(String)
    sport = Column(String)


class DeviceInformation(Base):
    __tablename__ = 'deviceInformation'
    id = Column(Integer, primary_key=True)
    profileId = Column(Integer, ForeignKey('profile.id'))
    operatingSystem = Column(String)
    displayResolution = Column(String)
    browser = Column(String)
    ISP = Column(String)
    adBlock = Column(Boolean)


class Cookies(Base):
    __tablename__ = 'cookies'
    id = Column(Integer, primary_key=True)
    profileId = Column(Integer, ForeignKey('profile.id'))
    sessionState = Column(Text)
    language = Column(String)
    region = Column(String)
    recentPages = Column(Text)
    productId = Column(Integer)
    productName = Column(String)
    productPrice = Column(Integer)
    quantity = Column(Integer)
    subTotal = Column(Integer)
    total = Column(Integer)
    couponCode = Column(String)
    shippingInformation = Column(Text)
    taxInformation = Column(Text)


class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    profileId = Column(Integer, ForeignKey('profile.id'))
    profileIds = Column(Text)
    basicDataIds = Column(Text)
    contactsIds = Column(Text)
    workAndEducationIds = Column(Text)
    placeOfResidenceIds = Column(Text)
    personalInterestsIds = Column(Text)


class WorkAndEducation(Base):
    __tablename__ = 'workAndEducation'
    id = Column(Integer, primary_key=True)
    profileId = Column(Integer, ForeignKey('profile.id'))
    placeOfWork = Column(String)
    skills = Column(Text)
    university = Column(String)
    faculty = Column(String)


class BasicData(Base):
    __tablename__ = 'basicData'
    id = Column(Integer, primary_key=True)
    profileId = Column(Integer, ForeignKey('profile.id'))
    interests = Column(Text)
    languages = Column(Text)
    religionViews = Column(String)
    politicalViews = Column(String)


def upgrade():
    op.create_table(
        'datasets',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('filename', sa.String(), nullable=True)
    )

    op.create_table(
        'profile',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('datasetsId', sa.String(), nullable=True),
        sa.Column('firstName', sa.String(), nullable=True),
        sa.Column('lastName', sa.String(), nullable=True),
        sa.Column('dateOfBirth', sa.String(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('email', postgresql.ARRAY(sa.String(), nullable=True)),
        sa.Column('phone', postgresql.ARRAY(sa.String() , nullable=True)),
        sa.Column('maritalStatus', sa.Integer(), nullable=True),
        sa.Column('income', sa.Integer(), nullable=True)
    )

    op.create_table(
        'credentials',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profileId', sa.Integer(), nullable=True),
        sa.Column('emails', sa.Text(), nullable=True),
        sa.Column('phones', sa.Text(), nullable=True)
    )

    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profileId', sa.Integer(), nullable=True),
        sa.Column('mobilePhone', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('linkedAccounts', postgresql.ARRAY(sa.String() , nullable=True)),
        sa.Column('website', sa.String(), nullable=True)
    )

    op.create_table(
        'placeOfResidence',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profileId', sa.Integer(), nullable=True),
        sa.Column('currentCity', sa.String(), nullable=True),
        sa.Column('birthPlace', sa.String(), nullable=True),
        sa.Column('otherCities', postgresql.ARRAY(sa.String() , nullable=True), nullable=True)
    )

    op.create_table(
        'personalInterests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profileId', sa.Integer(), nullable=True),
        sa.Column('briefDescription', sa.Text(), nullable=True),
        sa.Column('hobby', sa.String(), nullable=True),
        sa.Column('sport', sa.String(), nullable=True)
    )

    op.create_table(
        'deviceInformation',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profileId', sa.Integer(), nullable=True),
        sa.Column('operatingSystem', sa.String(), nullable=True),
        sa.Column('displayResolution', sa.String(), nullable=True),
        sa.Column('browser', sa.String(), nullable=True),
        sa.Column('ISP', sa.String(), nullable=True),
        sa.Column('adBlock', sa.Boolean(), nullable=True)
    )

    op.create_table(
        'cookies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profileId', sa.Integer(), nullable=True),
        sa.Column('sessionState', sa.Text(), nullable=True),
        sa.Column('language', sa.String(), nullable=True),
        sa.Column('region', sa.String(), nullable=True),
        sa.Column('recentPages',postgresql.ARRAY(sa.String() , nullable=True)),
        sa.Column('productId', sa.Integer(), nullable=True),
        sa.Column('productName', sa.String(), nullable=True),
        sa.Column('productPrice', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('subTotal', sa.Integer(), nullable=True),
        sa.Column('total', sa.Integer(), nullable=True),
        sa.Column('couponCode', sa.String(), nullable=True),
        sa.Column('shippingInformation', sa.Text(), nullable=True),
        sa.Column('taxInformation', sa.Text(), nullable=True)
    )

    op.create_table(
        'settings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('profileId', sa.Integer(), nullable=True),
        sa.Column('profileIds', postgresql.ARRAY(sa.Integer() , nullable=True)),
        sa.Column('basicDataIds', postgresql.ARRAY(sa.Integer() , nullable=True)),
        sa.Column('contactsIds', postgresql.ARRAY(sa.Integer() , nullable=True)),
        sa.Column('workAndEducationIds', postgresql.ARRAY(sa.Integer() , nullable=True)),
        sa.Column('placeOfResidenceIds', postgresql.ARRAY(sa.Integer() , nullable=True)),
        sa.Column('personalInterestsIds', postgresql.ARRAY(sa.Integer() , nullable=True))
    )

    op.create_table(
        'workAndEducation',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profileId', sa.Integer(), nullable=True),
        sa.Column('placeOfWork', sa.String(), nullable=True),
        sa.Column('skills', postgresql.ARRAY(sa.String() , nullable=True)),
        sa.Column('university', sa.String(), nullable=True),
        sa.Column('faculty', sa.String(), nullable=True)
    )

    op.create_table(
        'basicData',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profileId', sa.Integer(), nullable=True),
        sa.Column('interests', sa.Text(), nullable=True),
        sa.Column('languages', postgresql.ARRAY(sa.String() , nullable=True)),
        sa.Column('religionViews', sa.String(), nullable=True),
        sa.Column('politicalViews', sa.String(), nullable=True)
    )


def downgrade():
    op.drop_table('datasets')
    op.drop_table('profile')
    op.drop_table('credentials')
    op.drop_table('contacts')
    op.drop_table('placeOfResidence')
    op.drop_table('personalInterests')
    op.drop_table('deviceInformation')
    op.drop_table('cookies')
    op.drop_table('settings')
    op.drop_table('workAndEducation')
    op.drop_table('basicData')
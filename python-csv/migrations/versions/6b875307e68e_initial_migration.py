"""Initial migration

Revision ID: 6b875307e68e
Revises: 
Create Date: 2023-06-30 01:58:16.647297

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6b875307e68e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datasets',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('filename', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datasetsid', sa.UUID(), nullable=True),
    sa.Column('firstname', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('dateofbirth', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('email', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('phone', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('maritalstatus', sa.Integer(), nullable=True),
    sa.Column('income', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['datasetsid'], ['datasets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('basicdata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profileid', sa.Integer(), nullable=True),
    sa.Column('interests', sa.Text(), nullable=True),
    sa.Column('languages', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('religionviews', sa.String(), nullable=True),
    sa.Column('politicalviews', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['profileid'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profileid', sa.Integer(), nullable=True),
    sa.Column('mobilephone', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('linkedaccounts', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['profileid'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cookies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profileid', sa.Integer(), nullable=True),
    sa.Column('sessionstate', sa.Text(), nullable=True),
    sa.Column('language', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('recentpages', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('productid', sa.Integer(), nullable=True),
    sa.Column('productname', sa.String(), nullable=True),
    sa.Column('productprice', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('subtotal', sa.Integer(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.Column('couponcode', sa.String(), nullable=True),
    sa.Column('shippinginformation', sa.Text(), nullable=True),
    sa.Column('taxinformation', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['profileid'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('credentials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profileid', sa.Integer(), nullable=True),
    sa.Column('emails', sa.Text(), nullable=True),
    sa.Column('phones', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['profileid'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deviceinformation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profileid', sa.Integer(), nullable=True),
    sa.Column('operatingsystem', sa.String(), nullable=True),
    sa.Column('displayresolution', sa.String(), nullable=True),
    sa.Column('browser', sa.String(), nullable=True),
    sa.Column('isp', sa.String(), nullable=True),
    sa.Column('adblock', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['profileid'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('personalinterests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profileid', sa.Integer(), nullable=True),
    sa.Column('briefdescription', sa.Text(), nullable=True),
    sa.Column('hobby', sa.String(), nullable=True),
    sa.Column('sport', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['profileid'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('placeofresidence',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profileid', sa.Integer(), nullable=True),
    sa.Column('currentcity', sa.String(), nullable=True),
    sa.Column('birthplace', sa.String(), nullable=True),
    sa.Column('othercities', postgresql.ARRAY(sa.String()), nullable=True),
    sa.ForeignKeyConstraint(['profileid'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('profileid', sa.Integer(), nullable=True),
    sa.Column('profileids', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('basicdataids', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('contactsids', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('workandeducationids', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('placeofresidenceids', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('personalinterestsids', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.ForeignKeyConstraint(['profileid'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workandeducation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profileid', sa.Integer(), nullable=True),
    sa.Column('placeofwork', sa.String(), nullable=True),
    sa.Column('skills', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('university', sa.String(), nullable=True),
    sa.Column('faculty', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['profileid'], ['profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workandeducation')
    op.drop_table('settings')
    op.drop_table('placeofresidence')
    op.drop_table('personalinterests')
    op.drop_table('deviceinformation')
    op.drop_table('credentials')
    op.drop_table('cookies')
    op.drop_table('contacts')
    op.drop_table('basicdata')
    op.drop_table('profile')
    op.drop_table('datasets')
    # ### end Alembic commands ###
































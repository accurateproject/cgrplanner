# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('tplan',
                Field('name'),
                auth.signature,
)

db.define_table('timing',
                Field('tpid', 'reference tplan', readable=False, writable=False),
                Field('tag', unique=False),
                Field('years', 'list:integer', requires=IS_IN_SET(range(2000, 2100), multiple=True)),
                Field('months', 'list:integer', requires=IS_IN_SET(range(1,13), multiple=True)),
                Field('month_days', 'list:integer', requires=IS_IN_SET(range(1,32), multiple=True)),
                Field('week_days', 'list:integer', requires=IS_IN_SET(range(1,8), multiple=True)),
                Field('day_time', 'time'),
                auth.signature,
                format='%(tag)s'
)

db.define_table('destination',
                Field('tpid', 'reference tplan', readable=False, writable=False),
                Field('tag', unique=False),
                Field('dest_prefix'),
                auth.signature,
                format='%(tag)s'
)

db.define_table('rate',
                Field('tpid', 'reference tplan', readable=False, writable=False),
                Field('tag', unique=False),
                Field('connect_fee', 'double'),
                Field('rate', 'double'),
                Field('rate_unit'),
                Field('rate_increment'),
                Field('group_interval_start'),
                Field('rounding_method'),
                Field('rounding_decimals', 'integer'),
                auth.signature,
                format='%(tag)s'
)

db.define_table('destination_rate',
                Field('tpid', 'reference tplan', readable=False, writable=False),
                Field('tag', unique=False),
                Field('destinations_tag', 'reference destination'),
                Field('rates_tag', 'reference rate'),
                auth.signature,
                format='%(tag)s'
)

db.define_table('rating_plan',
                Field('tpid', 'reference tplan', readable=False, writable=False),
                Field('tag', unique=False),
                Field('destrates_tag', 'reference destination_rate'),
                Field('timing_tag', 'reference timing'),
                Field('weight', 'double'),
                auth.signature,
                format='%(tag)s'
)

db.define_table('rating_profile',
                Field('tpid', 'reference tplan', readable=False, writable=False),
                Field('loadid', readable=False, writable=False),
                Field('tenant'),
                Field('tor'),
                Field('direction'),
                Field('subject'),
                Field('activation_time', 'datetime'),
                Field('rating_plan_tag', 'reference rating_plan'),
                Field('fallback_subjects'),
                auth.signature,
                format='%(direction)s:%(tor)s:%(subject)s'
)

db.define_table('actions', #action is reserved
                Field('tpid', 'reference tplan', readable=False, writable=False),
                Field('tag', unique=False),
                Field('action_name'),
                Field('balance_type'),
                Field('direction'),
                Field('units', 'double'),
                Field('expiry_time', 'datetime'),
                Field('destination_tag', 'reference destination'),
                Field('rating_subject'),
                Field('balance_weight', 'double'),
                Field('extra_parameters'),
                Field('weight', 'double'),
                auth.signature,
                format='%(tag)s'
)

db.define_table('action_timing',
                Field('tpid', 'reference tplan', readable=False, writable=False),
                Field('tag', unique=False),
                Field('action_tag', 'reference actions'),
                Field('timing_tag', 'reference timing'),
                Field('weight', 'double'),
                auth.signature,
                format='%(tag)s'
)

db.define_table('action_trigger',
                Field('tpid', 'reference tplan', readable=False, writable=False),
                Field('tag', unique=False),
                Field('balance_type'),
                Field('direction'),
                Field('threshold_type'),
                Field('threshold_value', 'double'),
                Field('destination_tag'),
                Field('actions_tag', 'reference actions'),
                Field('weight', 'double'),
                auth.signature,
                format='%(tag)s'
)

db.define_table('account_actions',
                 Field('tpid', 'reference tplan', readable=False, writable=False),
                 Field('loadid', readable=False, writable=False),
                 Field('tenant'),
                 Field('account'),
                 Field('direction'),
                 Field('action_timings_tag', 'reference action_timing'),
                 Field('action_triggers_tag', 'reference action_trigger'),
                 auth.signature,
                 format='%(direction)s:%(tennant)s:%(account)s'
 )

a0, a1 = request.args(0), request.args(1)
TPlans = (db.tplan.created_by == auth.user_id)
Destinations = (db.destination.created_by == auth.user_id) & (db.destination.tpid == session.tpid)
Timings = (db.timing.created_by == auth.user_id) & (db.timing.tpid == session.tpid)
Rates = (db.rate.created_by == auth.user_id) & (db.rate.tpid == session.tpid)
DestinationRates = (db.destination_rate.created_by == auth.user_id) & (db.destination_rate.tpid == session.tpid)
RatingPlans = (db.rating_plan.created_by == auth.user_id) & (db.rating_plan.tpid == session.tpid)
RatingProfiles = (db.rating_profile.created_by == auth.user_id) & (db.rating_profile.tpid == session.tpid)
Actions = (db.actions.created_by == auth.user_id) & (db.actions.tpid == session.tpid)
ActionTimings = (db.action_timing.created_by == auth.user_id) & (db.action_timing.tpid == session.tpid)
ActionTriggers = (db.action_trigger.created_by == auth.user_id) & (db.action_trigger.tpid == session.tpid)
AccountActions = (db.account_actions.created_by == auth.user_id) & (db.account_actions.tpid == session.tpid)

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

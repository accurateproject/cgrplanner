# -*- coding: utf-8 -*-

def index():
    return dict()

@auth.requires_login()
def home():
    plans = db(TPlans).select()
    return locals()

@auth.requires_login()
def edit_plan():
    form = crud.update(db.tplan, a0, next=URL('home'))
    return locals()

@auth.requires_login()
def select_plan():
    session.tpid = a0
    session.flash = T('Plan successfully selected')
    redirect(URL('home'))

@auth.requires_login()
def manage():
    tpid = session.tpid
    if not tpid or not db.tplan(tpid):
        session.flash = T('Please select a plan')
        redirect(URL('home'))
    db.destination.tpid.default = tpid
    db.timing.tpid.default = tpid
    db.rate.tpid.default = tpid
    db.destination_rate.tpid.default = tpid
    db.rating_plan.tpid.default = tpid
    db.rating_profile.tpid.default = tpid
    db.actions.tpid.default = tpid
    db.action_timing.tpid.default = tpid
    db.action_trigger.tpid.default = tpid
    db.account_actions.tpid.default = tpid

    defined_tables = {
        'destinations': Destinations,
        'timings': Timings,
        'rates': Rates,
        'destination_rates': DestinationRates,
        'rating_plans': RatingPlans,
        'rating_profiles': RatingProfiles,
        'actions': Actions,
        'action_timings': ActionTimings,
        'action_triggers': ActionTriggers,
        'account_actions': AccountActions,
    }
    table = a0
    if not table in defined_tables:
        session.flash = T('Invalid table')
        redirect(URL('home'))
    title = " ".join(table.split("_")).title()
    grid = SQLFORM.grid(defined_tables[table],args=request.args[:1])
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downhtmling of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed html operator
      LOAD('default','data.html',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

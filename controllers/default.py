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
def destinations():
    tpid = session.tpid
    if not tpid or not db.tplan(tpid):
        session.flash = T('Please select a plan')
        redirect(URL('home'))
    title = T('Destinations')
    grid = SQLFORM.grid(Destinations)
    response.view = 'default/grid.html'
    return locals()

@auth.requires_login()
def timings():
    tpid = session.tpid
    if not tpid or not db.tplan(tpid):
        session.flash = T('Please select a plan')
        redirect(URL('home'))
    title = T('Timings')
    grid = SQLFORM.grid(Timings)
    response.view = 'default/grid.html'
    return locals()

@auth.requires_login()
def rates():
    title = T('Rates')
    grid = SQLFORM.grid(Rates)
    response.view = 'default/grid.html'
    return locals()

@auth.requires_login()
def destination_rates():
    tpid = session.tpid
    if not tpid or not db.tplan(tpid):
        session.flash = T('Please select a plan')
        redirect(URL('home'))
    title = T('DestinationRates')
    grid = SQLFORM.grid(DestinationRates)
    response.view = 'default/grid.html'
    return locals()

@auth.requires_login()
def rating_plans():
    tpid = session.tpid
    if not tpid or not db.tplan(tpid):
        session.flash = T('Please select a plan')
        redirect(URL('home'))
    title = T('RatingPlans')
    grid = SQLFORM.grid(RatingPlans)
    response.view = 'default/grid.html'
    return locals()

@auth.requires_login()
def rating_profiles():
    tpid = session.tpid
    if not tpid or not db.tplan(tpid):
        session.flash = T('Please select a plan')
        redirect(URL('home'))
    title = T('RatingProfiles')
    grid = SQLFORM.grid(RatingProfiles)
    response.view = 'default/grid.html'
    return locals()

@auth.requires_login()
def actions():
    tpid = session.tpid
    if not tpid or not db.tplan(tpid):
        session.flash = T('Please select a plan')
        redirect(URL('home'))
    title = T('Actions')
    grid = SQLFORM.grid(Actions)
    response.view = 'default/grid.html'
    return locals()

@auth.requires_login()
def action_timings():
    tpid = session.tpid
    if not tpid or not db.tplan(tpid):
        session.flash = T('Please select a plan')
        redirect(URL('home'))
    title = T('ActionTimings')
    grid = SQLFORM.grid(ActionTimings)
    response.view = 'default/grid.html'
    return locals()

@auth.requires_login()
def action_triggers():
    tpid = session.tpid
    if not tpid or not db.tplan(tpid):
        session.flash = T('Please select a plan')
        redirect(URL('home'))
    title = T('ActionTriggers')
    grid = SQLFORM.grid(ActionTriggers)
    response.view = 'default/grid.html'
    return locals()

@auth.requires_login()
def account_actions():
    tpid = session.tpid
    if not tpid or not db.tplan(tpid):
        session.flash = T('Please select a plan')
        redirect(URL('home'))
    title = T('AccountActions')
    grid = SQLFORM.grid(AccountActions)
    response.view = 'default/grid.html'
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

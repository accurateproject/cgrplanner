# -*- coding: utf-8 -*-

def index():
    text = 'cgrates'
    return locals()

def destinations():
    title = T('Destinations')
    grid = SQLFORM.grid(Destinations)
    response.view = 'default/grid.html'
    return locals()

def timings():
    title = T('Timings')
    grid = SQLFORM.grid(Timings)
    response.view = 'default/grid.html'
    return locals()

def rates():
    title = T('Rates')
    grid = SQLFORM.grid(Rates)
    response.view = 'default/grid.html'
    return locals()

def destination_rates():
    title = T('DestinationRates')
    grid = SQLFORM.grid(DestinationRates)
    response.view = 'default/grid.html'
    return locals()

def rating_plans():
    title = T('RatingPlans')
    grid = SQLFORM.grid(RatingPlans)
    response.view = 'default/grid.html'
    return locals()

def rating_profiles():
    title = T('RatingProfiles')
    grid = SQLFORM.grid(RatingPlans)
    response.view = 'default/grid.html'
    return locals()

def actions():
    title = T('Actions')
    grid = SQLFORM.grid(Actions)
    response.view = 'default/grid.html'
    return locals()

def action_timings():
    title = T('ActionTimings')
    grid = SQLFORM.grid(ActionTimings)
    response.view = 'default/grid.html'
    return locals()

def action_triggers():
    title = T('ActionTriggers')
    grid = SQLFORM.grid(ActionTriggers)
    response.view = 'default/grid.html'
    return locals()

def account_actions():
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
def downhtml():
    """
    allows downhtmling of uphtmled files
    http://..../[app]/default/downhtml/[filename]
    """
    return response.downhtml(request, db)


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

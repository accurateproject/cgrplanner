# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(IMG(_src='http://cgrates.org/img/bg/logo.png', _alt='CGRateS', _style='height:27px'), _class="brand",_href=URL('default', 'index'))
response.title = 'CGRPlanner'
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Radu Ioan Fericean <radu.fericean@itsyscom.com>'
response.meta.description = 'CGRateS rating plans creation tool'
response.meta.keywords = 'cgrates, rating, rates'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'home'), []),
    (T('Destinations'), False, URL('default', 'manage', args='destinations'), []),
    (T('Timings'), False, URL('default', 'manage', args='timings'), []),
    (T('Rates'), False, URL('default', 'manage', args='rates'), []),
    (T('DestinationRates'), False, URL('default', 'manage', args='destination_rates'), []),
    (T('RatingPlans'), False, URL('default', 'manage', args='rating_plans'), []),
    (T('RatingProfiles'), False, URL('default', 'manage', args='rating_profiles'), []),
    (T('Actions'), False, URL('default', 'manage', args='actions'), []),
    (T('ActionTimings'), False, URL('default', 'manage', args='action_timings'), []),
    (T('ActionTriggers'), False, URL('default', 'manage', args='action_triggers'), []),
    (T('AccountActions'), False, URL('default', 'manage', args='account_actions'), []),
]

if "auth" in locals(): auth.wikimenu() 

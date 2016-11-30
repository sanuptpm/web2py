from gluon.tools import Crud
import simplejson  
crud = Crud(db)
# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

def index():
    return dict()

def data():
    if not session.m or len(session.m)==10: session.m=[]
    if request.vars.q: session.m.append(request.vars.q)
    session.m.sort()
    return TABLE(*[TR(v) for v in session.m]).xml()

def companies():
    companies = db(db.company).select(orderby = db.company.name)
    return locals()

def contacts():
    company = db.company(request.args(0)) or redirect(URL('companies'))
    contacts = db(db.contact.company == company_id).select(orderby = db.contact.name)
    return locals()

@auth.requires_login()
def company_create():
    form = crud.create(db.company, next = 'companies')
    return locals()

@auth.requires_login()
def company_edit():
    company = db.company(request.args(0)) or redirect(URL('companies'))
    form = crud.update(db.company, company, next='companies')
    return locals()

@auth.requires_login()
def contact_create():
    db.contact.company.default = request.args(0)
    form = crud.create(db.contact, next = 'companies')
    return locals()

@auth.requires_login()
def contact_edit():
    contact = db.contact(request.args(0)) or redirect(URL('companies'))
    form = crud.update(db.contact, contact, next = 'companies')
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
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
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




def hello6():
    response.flash=T("hello")
    return dict(message=T("welcome app"))

def redirectme():
    redirect(URL('hello6'))

def raisexception():
    1/0
    return "oooooooo"

def servejs():
    import gluon.contenttype
    response.headers['Content-type']=gluon.contenttype.contenttype('.js')
    return 'alert("fdgdfgdg dfg fdg fg ");'

def makejson():
    return response.json(['sd', {'ds':(2,'ds')}])

def counter():
    session.counter = (session.counter or 0) + 1
    return dict(counter=session.counter)

def test_def():
    return dict()

def civilized():
    response.menu=[['civilized',True,URL('civilized')],
                   ['slick',False,URL('slick')],
                   ['basic',False,URL('basic')]]
    response.flash='you clicked on civilized'
    return dict(message="you clicked on civilized")

def form():
    form = FORM(TABLE(TR("Your name:",INPUT(_type="text",_name="name",requires=IS_NOT_EMPTY())),
                    TR("Your email:",INPUT(_type="text",_name="email",requires=IS_EMAIL())),
                    TR("Admin",INPUT(_type="checkbox",_name="admin")),
                    TR("Sure?",SELECT('yes','no',_name="sure",requires=IS_IN_SET(['yes','no']))),
                    TR("Profile",TEXTAREA(_name="profile",value="write something here")),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))

    if form.accepts(request,session):
        response.flash="form accepted"
    elif form.errors:
        response.flash="form is invalid"
    else:
        response.flash="please fill the form"
    return dict(form=form,vars=form.vars)









response.menu = [['Register Person', False, URL('register_person')],
                 ['Register Product', False, URL('register_product')],
                 ['Buy product', False, URL('buy')]]

def register_person():
    # create an insert form from the table
    form = SQLFORM(db.person).process()

    # if form correct perform the insert
    if form.accepted:
        response.flash = 'new record inserted'

    # and get a list of all persons
    records = SQLTABLE(db().select(db.person.ALL),headers='fieldname:capitalize')

    return dict(form=form, records=records)

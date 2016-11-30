# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

POSTS_PER_PAGE = 10

def get_category():
    category_name = request.args(0)
    category = db.category(name=category_name)
    if not category:
        session.falsh = "Page not found"
        redirect(URL('index'))
    return category

def index():
    rows = db(db.category).select()
    return locals()

def create_post():
    category = get_category()
    db.post.category.default = category.id
    form = SQLFORM(db.post).process(next='view_post/[id]')
    return locals()

def edit_post():
    id = request.args(0, cast=int)
    form = SQLFORM(db.post, id).process(next='view_post/[id]')
    return locals()

def list_post_by_datetime():
    category = get_category()
    page = request.args(1, cast=int, default=0)
    start = page*POSTS_PER_PAGE 
    stop = start+POSTS_PER_PAGE
    rows = db(db.post.category==category.id).select(orderby=~db.post.created_on,
        limitby=(start,stop))
    return locals()

def list_posts_by_votes():
    category = get_category()
    page = request.args(1, cast=int, default=0)
    start = page*POSTS_PER_PAGE 
    stop = start+POSTS_PER_PAGE
    rows = db(db.post.category==category.id).select(orderby=~db.post.votes,
        limitby=(start,stop))
    return locals()

def list_posts_by_author():
    user_id = request.args(0, cast=int)
    page = request.args(1, cast=int, default=0)
    start = page*POSTS_PER_PAGE 
    stop = start+POSTS_PER_PAGE
    rows = db(db.post.created_by==user_id).select(orderby=~db.post.created_on,
        limitby=(start,stop))
    return locals()

def view_post():
    id = request.args(0, cast=int)
    post = db.post(id) or redirect(URL('index'))
    comments = db(db.comm.post==post.id).select(orderby=~db.comm.created_on)
    return locals()

def vote_callback():
    id = request.args(0, cast=int)
    direction = request.args(1)
    return locals()

def comm_vote_callback():
    id = request.args(0, cast=int)
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



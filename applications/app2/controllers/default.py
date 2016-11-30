# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
import os

import cStringIO
 
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def generatepdf():
    rows = db(db.blog_post).select(orderby=db.blog_post.title.upper())
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Hello World", styles['Heading1']),
        Paragraph("The quick brown fox", styles['Normal']),
        Spacer(1, 0.25*inch),
        Paragraph("First PDF Doc.", styles['Normal']),
        Paragraph(rows[0]['title'], styles['Normal'])]
    buffer = cStringIO.StringIO()   
    doc = SimpleDocTemplate(buffer)
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
   
    filename = request.args(0)
    if filename:
        header = {'Content-Disposition': 'attachment; filename=' + filename}
    else:
        header = {'Content-Type': 'application/pdf'}
    response.headers.update(header)
    return pdf


def index():  
    rows = db(db.blog_post).select(orderby=db.blog_post.title.upper())
    return locals()


@auth.requires_login()    
def create():
    form = SQLFORM(db.blog_post).process()
    if form.accepted:
        session.flash = "Blog is Posted"
        redirect(URL('index'))
    return locals()

@auth.requires_login()
def show():
    post = db.blog_post(request.args(0, cast=int))
    db.blog_comment.blog_post.default = post.id
    db.blog_comment.blog_post.readable = False
    db.blog_comment.blog_post.writable = False
    form = SQLFORM(db.blog_comment).process()
    comments = db(db.blog_comment.blog_post==post.id).select()
    return locals()

@auth.requires_membership('managers')
def manage():
    grid = SQLFORM.grid(db.blog_post)
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

def test():
    form = SQLFORM(db.test).process()
    if form.accepted:
        session.flash = "Blog is Posted"
        redirect(URL('index'))
    return locals()


@request.restful()
def api():
    response.view = 'generic.'+request.extension
    def GET(*args,**vars):
        print "====args==", args
        print "====vars===", vars
        patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)
    def POST(table_name,**vars):
        return db[table_name].validate_and_insert(**vars)
    def PUT(table_name,record_id,**vars):
        return db(db[table_name]._id==record_id).update(**vars)
    def DELETE(table_name,record_id):
        return db(db[table_name]._id==record_id).delete()
    return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)



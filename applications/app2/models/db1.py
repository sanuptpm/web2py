# auth.signature add default fields like the created on/ create by/ modified by/ modified on
db.define_table('blog_post',
	Field('title', requires=IS_NOT_EMPTY()),
	Field('body', 'text', requires=IS_NOT_EMPTY()),
	Field('photo', 'upload'), 
	auth.signature)

db.define_table('blog_comment',
	Field('blog_post', 'reference blog_post'),
	Field('comments', 'text', requires=IS_NOT_EMPTY()),
	auth.signature
	)
db.blog_post.title.requires = IS_NOT_IN_DB(db, db.blog_post.title)

db.define_table('test',
    Field('first_name', requires = IS_NOT_EMPTY()),
    Field('last_name', requires = IS_NOT_EMPTY()),
    Field('email', requires= IS_EMAIL()),
    Field('email_validate',requires = IS_EQUAL_TO(request.vars.email)))

db.define_table("entries", Field("entry", "text")) 


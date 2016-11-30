# auth.signature add default fields like the created on/ create by/ modified by/ modified on
db.define_table('blog_post',
	Field('title', requires=IS_NOT_EMPTY()),
	Field('body', 'text', requires=IS_NOT_EMPTY()),
	auth.signature)

db.define_table('blog_comment',
	Field('blog_post', 'reference blog_post'),
	Field('comments', 'text', requires=IS_NOT_EMPTY()),
	auth.signature
	)

db.define_table('the_aliaser',
                Field('name',
                      type='string',
                      label=T('Name')),
                Field('description',
                      type='text',
                      label=T('Description')),
                Field('the_url',
                      type='string',
                      label=T('The URL')),
                Field('the_slug',
                      unique=True,
                      type='string',
                      label=T('Slug Name')),
                Field('alias_url',
                      type='string',
                      label=T('Alias URL'))
                )

db.the_aliaser.the_slug.compute = lambda row: IS_SLUG(keep_underscores=False)(row.name)[0]
db.the_aliaser.name.requires = IS_NOT_IN_DB(db, db.the_aliaser.name)
db.the_aliaser.alias_url.compute = lambda row: request.env.http_host + '/aliaser/default/resolve_alias/' + row.the_slug
#!venv/bin/python

# Creates a new post entry
def create(config):
    from app import create_slug

    template = 'page' if config.template == None else config.template

    vars = {
        'title'   : config.title,
        'template': template,
        'tags'    : config.tags,
        'date'    : datetime.now().strftime('%Y-%m-%d')
    }

    new_post_template = \
"""{%% extends "%(template)s.html" %%}
{%% set page_title = "%(title)s" %%}
{%% set page_description = "%(title)s" %%}
{%% set post_tags = "%(tags)s" %%}
{%% set post_date = "%(date)s" %%}
{%% set disable_comments = False %%}

{%% block page_content %%}
    {{ macros.post_base({'title': page_title, 'date': post_date, 'tags': post_tags}, lang, vars) }}
    <p>Mussum ipsum cacilds, vidis litro abertis. Consetis adipiscings elitis. 
    Pra lá , depois divoltis porris, paradis. Paisis, filhis, espiritis santis. 
    Mé faiz elementum girarzis, nisi eros vermeio, in elementis mé pra quem é 
    amistosis quis leo. Manduma pindureta quium dia nois paga. Sapien in monti 
    palavris qui num significa nadis i pareci latim. Interessantiss quisso pudia 
    ce receita de bolis, mais bolis eu num gostis.</p>
{%% endblock %%}""" % vars

    file_name = config.lang + '/' + create_slug(config.title) + '.html'

    try:
        with open('templates/pages/' + file_name, 'w') as new_file:
            new_file.write(new_post_template)
    except Exception, e:
        raise e
    else:
        print "\n>>> New post created: %s\n" % file_name
        return file_name

# Updates the index file with a new node representing the new post
def update_index(node):
    import json

    try:
        with open('posts.json', 'rw+') as json_file:
            index = json.load(json_file)

            # append the new node to the key that corresponds to the language
            index['posts'][node['lang']].append(node)

            # set the file pointer to the beginning
            json_file.seek(0)

            json.dump(index, json_file, indent = 4)
    except Exception, e:
        raise e
    else:
        return index

# Parse command line arguments
def parse_args():
    import argparse

    desc = \
    """This is a generator that creates new posts for the blog.
    Example of usage:
    new_post.py -l en -tt 'Creating a new post!' -tg 'python,flask,fancytag'
    """

    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument('-l', '--lang', help = 'Post language', required = True)
    parser.add_argument('-tt', '--title', help = 'Post title', required = True)
    parser.add_argument('-tg', '--tags', help = 'Post tags (separated by commas)', required = True)
    parser.add_argument('-tp', '--template', help = 'Template used', required = False)
    parser.add_argument('-no', '--noupdate', action='store_true', help = "Don't update index", required = False)

    return parser.parse_args()

if __name__ == '__main__':
    from datetime import datetime

    try:
        args      = parse_args()
        file_name = create(args)
        new_node  = {
            'date' : datetime.now().strftime('%Y-%m-%d'),
            'title': args.title,
            'lang' : args.lang,
            'uri'  : '/' + file_name,
            'tags' : args.tags
        }

        if args.noupdate == False:
            update_index(new_node)
            print ">>> Posts index successfully updated with entry: \n{0}\n".format(new_node)
    except Exception, e:
        raise e
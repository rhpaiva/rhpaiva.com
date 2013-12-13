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
{%% set page_description = "" %%}
{%% set post_tags = "%(tags)s" %%}
{%% set post_date = "%(date)s" %%}
{%% set disable_comments = False %%}

{%% block page_content %%}
    {{ macros.post_base({'title': page_title, 'date': post_date, 'tags': post_tags}, lang, vars) }}
    <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. 
    Eum, quos, dolores, pariatur sint impedit atque repellat odit ad minima 
    dolorem quia ipsa porro consequatur qui expedita. Qui, repellat alias non 
    iste minima hic laboriosam minus recusandae quos exercitationem sapiente 
    et optio dignissimos vitae consequatur esse porro consectetur sit eveniet 
    mollitia voluptate delectus odio tempore eaque aspernatur adipisci 
    quisquam suscipit rerum quasi possimus aperiam iusto ipsum reiciendis 
    architecto sunt fugit iure maiores expedita voluptates ullam pariatur vel 
    deserunt vero dolor omnis molestias?</p>
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
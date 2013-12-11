#!venv/bin/python

# Creates a new post entry
def create(config):
    from app import create_slug

    template = 'page' if config.template == None else config.template

    new_post_template  = '{%% set page_title = "%s" %%}' % config.title
    new_post_template += '\n{% set page_description = "description" %}'
    new_post_template += '\n{%% extends "%s.html" %%}' % template
    new_post_template += \
    """

    {% block page_content %}
    <article>
        <h1>{{page_title}}</h1>
        contento!
    </article>
    {% endblock %}"""

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

    desc = 'This is a generator that creates new posts for the blog'

    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument('-l', '--lang', help = 'Post language', required = True)
    parser.add_argument('-t', '--title', help = 'Post title', required = True)
    parser.add_argument('-tp', '--template', help = 'Template used', required = False)
    parser.add_argument('-n', '--noupdate', action='store_true', help = "Don't update index", required = False)

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
            'uri'  : '/' + file_name
        }

        if args.noupdate == False:
            update_index(new_node)
            print ">>> Posts index successfully updated with entry: \n{0}\n".format(new_node)
    except Exception, e:
        raise e
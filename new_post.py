#!venv/bin/python

# Creates a new post entry
def create(config):

    template = 'post' if config.template == None else config.template

    new_post_template  = '{%% set post_title = "%s" %%}' % config.title
    new_post_template += '\n{%% extends "%s.html" %%}' % template
    new_post_template += '\n\n{% block post_content %}\npost content\n{% endblock %}'

    file_name = config.lang + '/' + config.title + '.html'

    try:
        with open('templates/posts/' + file_name, 'w') as new_file:
            new_file.write(new_post_template)
    except Exception, e:
        raise e
    else:
        print "\n>>> New post created: %s" % file_name
        return file_name

# Updates the index file with a new node representing the new post
def update_index(node):
    from app import read_json
    import json

    index = read_json('index.json')

    index['posts'].append(node)

    try:
        with open('index.json', 'w+') as json_file:
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

    return parser.parse_args()

if __name__ == '__main__':
    from datetime import datetime

    try:
        args      = parse_args()
        file_name = create(args)
        new_node  = {
            'date' : datetime.now().strftime('%Y-%m-%d'),
            'title': args.title,
            'uri'  : '/' + file_name
        }

        index = update_index(new_node)        
    except Exception, e:
        raise e

    print "\n>>> Posts index successfully updated with entry: {0}\n".format(new_node)

    #update_index(new_node['posts'])
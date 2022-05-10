#!/usr/bin/python3
import cgitb
import cgi
import shelve
import sys
from html import escape
from os import environ


sys.path.insert(len(sys.path)+1, '/home/tepes/PycharmProjects/tkinter_example')

from main import User

print('Content-type: text/html\n')
print()

def save(db, key, name, age):
    if key not in db:
        db[key] = User(name, age)


def delete(db, key):
    if key in db:
        del db[key]


def change(db, key, name, age):
    if key in db:
        rec = db[key]
        setattr(rec, 'name', name)
        setattr(rec, 'age', age)
        db[key] = rec


cgitb.enable()

form_data = cgi.FieldStorage()
db = shelve.open('db')
html = open('./index.html').read()
fields = ['name', 'age']
data = ''
row = """
    <tr><th>$NAME$</th><td><input type="text" name="$NAME$" value="$VALUE$"></td></tr>
"""

QUERY_STRING = environ.get('QUERY_STRING')

current_key = str(form_data['current_key'].value) if 'current_key' in form_data else None

post_query_param = {
    'key': escape(form_data['key'].value if 'key' in form_data else ''),
    'name': escape(form_data['name'].value if 'name' in form_data else ''),
    'age': escape(form_data['age'].value if 'age' in form_data else '')
}

if 'action' in form_data:
    action = form_data['action'].value
    if action == 'add':
        save(db, **post_query_param)
    elif action == 'delete':
        delete(db, post_query_param['key'])
    elif action == 'change':
        change(db, **post_query_param)


if type(current_key) is str and current_key in db:
    html = html.replace('$KEY$', current_key)
    rec = db[current_key]
    for field in fields:
        data += row.replace('$NAME$', str(field)).replace('$VALUE$', getattr(rec, str(field)))
else:
    for field in fields:
        data += row.replace('$NAME$', field)


html = html.replace('$FORM$', data)

all = ''
for index, db_key in enumerate(db):
    href = f'py-cgi.py?current_key={db_key}'
    if current_key == db_key:
        all += f'<tr style="background: red; color: yellow;"><td><a style=" color: yellow;" href="{href}">{db_key}</a>'
    else:
        all += f'<tr><td><a href="{href}">{db_key}</a>'

    for field in fields:
        value = str(getattr(db[db_key], field))
        all += f'<td><a>{value}</a></td>'

    all += '</tr>'


html = html.replace('$ALL$', all)

for var in ['$KEY$', '$FORM$', '$NAME$', '$VALUE$']:
    html = html.replace(var, '')

db.close()


print(html)
print()

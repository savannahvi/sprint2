from flask import Flask
from flask import request
import re
import os
import json
import sys

app = Flask(__name__)

prefix = sys.argv[1]
write_dir = '/svr/runme/' + prefix + '/'

@app.route('/', methods=['POST'])
def receiveJSON():
    ### returns a list of all keys in a dictionary
    ### used in no_dupe_keys
    def extract_keys(d):
        keys = []
        for k, v in d.items():
            if isinstance(v, dict):
                keys = keys + extract_keys(v)
        return list(d.keys()) + keys

    ### recursively search a dictionary for key repeats
    ### if no repeats found, returns true
    def no_dupe_keys(d):
        keys_list = extract_keys(d)

        ct_a = 0
        ct_n = 0
        for i in keys_list:
            if i == 'age':
                ct_a += 1
            if i == 'name':
                ct_n += 1

        if ct_a == 1 and ct_n == 1:
            return (True)
        else:
            return (False)

    ### checks to see if file already exists
    ### returns 'a' for append if it does, 'w' otherwise
    def app_or_writ(dir_, f):
        if os.path.exists(dir_ + f):
            return 'a'
        else:
            return 'w'

    ### takes the post-request object and writes to raw file
    def write_raw(write_dir, content):
        with open(write_dir + 'Raw.txt', app_or_writ(write_dir, 'Raw.txt')) as f:
            f.write(str(content)+'\n')

    ### processes the blob and writes to proc file
    def write_proc(write_dir, content):
        try:
            name, age = content['name'], content['prop']['age']

            try:
                int(age)
            except ValueError as e:
                print('age is not an int')
                return ''

            if name != "" and age != "" and no_dupe_keys(content) and int(age) > 0:
                outputs = str(name) + ' ' + str(age)

                with open(write_dir + 'Proc.txt', app_or_writ(write_dir, 'Proc.txt')) as f:
                    f.write(outputs + '\n')

        except KeyError as e:
            print e

    ###  Loads the request into dictionary if possible
    content = request.get_json(silent = True)
    print content
    if content is None:
        print('not good')
    else:
        write_raw(write_dir, content)
        write_proc(write_dir, content)

    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

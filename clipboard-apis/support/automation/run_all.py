import glob
import json
import os
import re
from marionette_single_test import marionette_single_test

results = {}
dirname = os.path.dirname(os.path.realpath(__file__))
print dirname
for fn in glob.glob(os.path.join(dirname, '..', '..', '*.htm*')):
    fn = os.path.realpath(fn)
    fn = fn.replace('\\', '/')
    rx = re.compile('.*clipboard-apis')
    fn = re.sub(rx, 'http://localhost:8000/clipboard-apis', fn)
    try:
        results[fn] = marionette_single_test(fn)
    except Exception,e:
        results[fn] = str(e)

print json.dumps(results, indent=4)

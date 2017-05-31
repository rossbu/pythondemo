import json
import re

def is_MD5(s):
    return True if re.match(r"([a-f\d]{32})", key) else False

strr = '''
{
    "REQUEST": "FOUND",
    "739c5b1cd5681e668f689aa66bcc254c": {
        "plain": "test",
        "hexplain": "74657374",
        "algorithm": "MD5X5PLAIN"
    }
}
'''

parsed_json = json.loads(strr)

for key, value in parsed_json.items():
    if is_MD5(key) and 'plain' in parsed_json[key]:
        xHash = key
        xPlain = parsed_json[key]['plain']

        print('value in key "plain" in key "{0}" is "{1}"'.format(*[xHash,xPlain]))
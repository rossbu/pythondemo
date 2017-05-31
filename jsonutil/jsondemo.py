import json

json_string = '''
{
    "REQUEST": "FOUND",
    "739c5b1cd5681e668f689aa66bcc254c": {
        "plain": "test",
        "hexplain": "74657374",
        "algorithm": "MD5X5PLAIN"
    }
}
'''

if '746' in json_string:
    parsed_json = json.loads(json_string)
    print(parsed_json['739c5b1cd5681e668f689aa66bcc254c']['plain'])

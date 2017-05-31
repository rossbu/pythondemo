from __future__ import print_function
import json, base64
import requests
import glob, os

filenamearray = []
simplenamearray = []
for file in os.listdir("C:/Users/username/dev/Active/search/PDF"):
    if file.endswith(".pdf"):
        filename = os.path.join("C:/Users/username/dev/Active/search/PDF", file)
        filenamearray.append(filename)
        simplenamearray.append(file)

for index, elem in enumerate(filenamearray):
    print(index, elem)
    afile = open(elem, "rb")
    file64 = base64.b64encode(afile.read()).decode('ascii')
    f = open('tmp.json', 'w')
    location = 'righthere'
    data_0 = {"index": {"_index": "myindex", "_type": "document", "_id": str(100+index)}}
    data_1 = {"thedata": file64, "title": simplenamearray[index], "location": location}
    json.dump(data_0, f)
    print("", file=f)
    json.dump(data_1, f)
    print("", file=f)
    f.close()
    with open('tmp.json', 'r') as myfile:
        data = myfile.read()
        headers = {"Content-Type": "application/json"}
        response = requests.put('http://es.companyname.net:9200/_bulk?pipeline=attachment', data=data, headers=headers)
        print(response.text)

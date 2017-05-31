from datetime import datetime
import getopt
import httplib
import json
from json2html import *
import logging
import re
import requests
import sys
import tzlocal
import urlparse
import urllib
import thread
import time

__author__ = 'tbu'
__version__ = '1.0'


def __init__(self):
    self.__opr = 'changelog'
    self.__dict__ = {}


def getchangelog(jenkinsjoburl, lastbuildnumber, giturl, gitbranch, builduser, changelogfile, jiraurl):
    # giturl=https://companyname@bitbucket.org/project/test-repository.git  # assume this always ends with '.git' so need to strip off
    # jenkinsurl = "https://xxxx.yyyy.net/jenkins/"
    # changelogfile="jbchangelog.html"
    """jenkinsjoburl needs to be provided"""
    if giturl.endswith('.git'):
        giturl = giturl[:-4]
        # giturl = re.sub('\.git$', '', giturl)

    print "Starts Building with jenkinsjoburl (quoted) : " + urllib.quote(jenkinsjoburl)
    with open(changelogfile, "a") as f:
        f.write('<!DOCTYPE html>')
        f.write('<html>')
        f.write('<head>')
        f.write("<title>Jenkins Change Log</title>")
        # f.write('<link rel="stylesheet"  type="text/css" href="https://setools.s3.amazonaws.com/json2html.css" />')
        f.write('<meta name="viewport" content="width=device-width, initial-scale=1" />')
        f.write('<style type="text/css">')
        f.write('body { background-color: #fbfcf4; } ')
        f.write("</style>")
        f.write("</head>")

        f.write('<body>')

        f.write('<div style="text-align:center; border:1px solid lightblue; ">')
        f.write('<H1>Change Log</H1><br/>')
        # f.write('Author: BU<br/>')
        f.write('<div style="text-align:left;">')
        f.write('<B>Repos: </B> ' + giturl)
        f.write('<br/>')
        f.write('<B>Branch: </B> ' + gitbranch)
        f.write('<br/>')
        f.write('</div>')
        f.write('</div>')

        f.write('<div>')
        for m in range(1, int(lastbuildnumber) + 1)[::-1]:  # For loop is use here // actions[1].causes[0].userName
            requesturl = jenkinsjoburl + "/" + str(
                m) + "/api/json?tree=changeSet[items[msg,date,commitId,author[fullName]]],url,timestamp,actions[causes[userName]]"
            print requesturl
            resp = requests.get(requesturl)
            # print "text is : " + resp.text.encode('utf-8')

            if resp.status_code != 404:
                json_data = json.loads(resp.text)
                lengthofitems = len(json_data['changeSet']['items'])
                unix_timestamp = float(json_data['timestamp']) / 1000.0
                local_timezone = tzlocal.get_localzone()  # get pytz timezone
                local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
                print 'job# ' + str(m)
                try:
                    if 'UpstreamCause' in resp.text:
                        print '********* + UpstreamCause *************'
                        username = 'Upstream job'
                    elif 'ParametersAction' in resp.text:
                        print '********* + ParametersAction *************'
                        username = json_data['actions'][1]['causes'][0]['userName']
                    elif 'CauseAction' in resp.text:
                        username = json_data['actions'][0]['causes'][0]['userName']
                    else:
                        username = 'unknown'
                except (ValueError, KeyError, TypeError):
                    print "Unexpected error:", sys.exc_info()[0]
                    pass

                # print 'user is : ' + username
                buildheader = "<br/><H1>#" + str(m) + " ( " + local_time.strftime(
                    "%Y-%m-%d %H:%M:%S") + " ) - By [" + username + "]</H1><br/>"
                # print buildheader
                f.write(buildheader)

                f.write("<ul>")
                if lengthofitems != 0:
                    for n in range(0, lengthofitems):
                        f.write("<li>")
                        fullmsg = json_data['changeSet']['items'][n]['msg'].encode('utf-8')
                        if fullmsg:
                            # print "fullmsg : " + fullmsg
                            values = fullmsg.split(" ", 1)  # fullmsg.split(sep=" ", maxsplit=n)
                            # print "length of splited message : " + len(values)
                            try:
                                jiranumber = values[0]
                            except IndexError:
                                jiranumber = "BrokenCommitedMessage"
                            try:
                                puremsg = values[1]
                            except IndexError:
                                puremsg = ""

                            if "-" in jiranumber:
                                fulljiraurl = jiraurl + jiranumber
                                msgwithjiralink = "<a href='" + fulljiraurl + "' target='_blank'>" + jiranumber + "</a>" + " " + puremsg
                                # print "msg with jira link : " + msgwithjiralink
                                f.write(msgwithjiralink)
                            else:
                                # print "--- bad commited message without jira number ---"
                                f.write(fullmsg)
                        else:
                            f.write(fullmsg)

                        f.write(" -- ")
                        f.write(json_data['changeSet']['items'][n]['author']['fullName'])
                        f.write(" -- ")
                        f.write("<a href='" + giturl + "/commits/" + json_data['changeSet']['items'][n][
                            'commitId'] + "' target='_blank'>View Commit</a>")
                        f.write("</li>")
                else:
                    f.write("<li>No Changes in the build</li>")
                f.write("</ul>")
        f.write('</div>')
        f.write("</body></html>")


if __name__ == "__main__":
    print "This only executes when %s is executed rather than imported" % __file__
    getchangelog("https://wwww.company.net/jenkins/job/ddd%20FrontEnd%20on%20dev.company.net", "jobnumber",
                 "giturl", "dev", "someone",
                 "jbchangelog.html", "https://jira.company.net/browse/")
    print "Job is finished"
else:
    print 'This Module is being imported from another module'

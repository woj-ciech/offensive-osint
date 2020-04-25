from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import requests
import json
import math
import email.message
import smtplib
# default connects to localhost
es = Elasticsearch()

es.indices.create(index='rdp-monitoring', ignore=400)

SHODAN_API_KEY = ""
query = "port:3389 org:hospital"
endpoint = "https://api.shodan.io/shodan/host/search?key="+SHODAN_API_KEY+"&query="+query+"&page="
cve = "CVE-2019-0708"
fresh = []

def exists(ip):
    try:
        es.get(index='rdp-monitoring', id=ip)
        return True
    except:
        return False

def send_notification(ips):
    body = "<h1>New IPs in hospitals with Bluekeep</h1><br>"
    ips_text = ""

    for ip in ips:
        ips_text = ips_text + "https://beta.shodan.io/host/" + ip + "<br>"


    msg = email.message.Message()
    msg['Subject'] = 'RDP Monitoring'
    msg['From'] = "@gmail.com"
    msg['To'] = "@gmail.com"
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body + ips_text)

    gmail_user = "@gmail.com"
    gmail_password = ""

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        server.close()

        print('Email sent!')
    except Exception as e:
        print(e)
        print('Something went wrong...')
    pass

try:
    shodan_request = requests.get(endpoint)
    shodan_json = json.loads(shodan_request.text)
    for result in shodan_json['matches']:
        if not exists(result['ip_str']):
            check_each_host = requests.get("https://api.shodan.io/shodan/host/" + result['ip_str'] + "?key=" + SHODAN_API_KEY)
            check_each_host_json = json.loads(check_each_host.content)
            if 'vulns' in check_each_host_json:
                if cve in check_each_host_json['vulns']:
                    fresh.append(result['ip_str'])
                    print("New IP:" + result['ip_str'])
                    es.index(index="rdp-monitoring", id=check_each_host_json['ip_str'], body={"organization": check_each_host_json['org']})
        else:
            print("IP exists")

    if fresh:
        send_notification(fresh)

except Exception as e:
    print(e)



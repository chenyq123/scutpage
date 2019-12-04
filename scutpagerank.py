from queue import Queue
import networkx as nx

def getBaseURL(url):
    import re
    baseurl = re.findall("(https?://.*?)/", url)
    if baseurl:
        return baseurl[0]
    return url
    # return ""


def getLinkURL(url):
    import requests
    import re

    try:
        res = requests.get(url, timeout=1)
    except:
        return []

    res.encoding = 'utf-8'
    pat1 = "<a href=\"(https?.[\.a-zA-Z0-9/]*?\.scut\..[\.a-zA-Z0-9/]*)\""
    pat2 = "<a href=\"(/.[\.a-zA-Z0-9/]*?.htm)\""

    baseurl = getBaseURL(url)

    items = re.findall(pat1, res.text)
    items2 = re.findall(pat2, res.text)
    for item in items2:
        items.append(baseurl + item)
    return items


url = "https://www.scut.edu.cn/new/"

q = Queue(maxsize=0)
q.put(url)
urlnum = 1
urldict = {}
G = nx.DiGraph()
while not q.empty():
    u = q.get()
    G.add_node(u)
    linkurls = getLinkURL(u)
    for item in linkurls:
        G.add_edge(u, item)
        if not urldict.__contains__(item):
            urldict[item] = urlnum
            urlnum = urlnum + 1
            print(item)
            q.put(item)
nx.write_adjlist(G, "scuturlGraph")

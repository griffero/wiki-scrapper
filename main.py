from BeautifulSoup import BeautifulSoup
from robobrowser import RoboBrowser
import matplotlib.pyplot as plt
import networkx as nx
import thread

browser = RoboBrowser(history=True, parser='html5lib')
first_url = "https://en.wikipedia.org/wiki/Internet"

def get_anchors_from_url(url):
    browser.open(url)
    main_section = browser.select('.mw-parser-output')
    print "GET: ", url
    anchors = []
    for element in main_section:
        element = element.encode('utf-8').__str__()
        element = BeautifulSoup(element)
        el = element.findAll('div',{ "class" : "reflist" })
        if len(el) > 0:
            break
        else:
            _anchors = element.findAll('a', href=True)
            for anchor in _anchors:
                if type(anchor) is not list:
                    anchor = anchor['href'].split('/')
                    if len(anchor) > 1:
                        if anchor[1] == 'wiki':
                            if '.jpg' not in anchor[2] and '.png'not in anchor[2] and '.svg' not in anchor[2] and '(disambiguation)' not in anchor[2]:
                                anchor = 'https://en.wikipedia.org/wiki/' + anchor[2]
                                anchors.append(anchor)
    return anchors

first_anchors = get_anchors_from_url(first_url)
definitive_list = {}
definitive_list[first_url] = first_anchors[:30]

deep = 2
counter = 0
print "Scrapper started: "
while deep > counter:
    print "Deep: ", str(counter) + '/' + str(deep)
    for key in definitive_list.keys():
        for link in definitive_list[key]:
            if link not in definitive_list:
                anchors = get_anchors_from_url(link)[:30]
                if link not in definitive_list:
                    definitive_list[link] = anchors
                else:
                    print 'Repeated element: ', link
            else:
                print 'Repeated element: ', link
    counter +=1

graph = nx.Graph()
print "Drawing Graph"
for key in definitive_list:
    _key = key.split('/')[-1]
    graph.add_node(_key)
    for link in definitive_list[key]:
        _link = link.split('/')[-1]
        graph.add_node(_link)
        print "Adding Node: ", _link
        if graph.has_edge(_key, _link):
            print "Updating weight between: ", _link
            current_weight = graph[_key][_link]['weight']
            updated_weight = current_weight + 1
            graph[_key][_link]['weight'] = updated_weight
        else:
            print "Adding edge : ", str(_key) + ' ' + str(_link)
            graph.add_edge(_key,_link, weight = 1)


nx.draw(graph, with_labels=True, font_weight='bold')
plt.show()

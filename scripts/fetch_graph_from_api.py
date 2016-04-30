import requests
import networkx as nx
from nxpd import draw
from socialgraph.socialgraph import  elect_committee, paint_graph

# WARNING: This version is ignoring topics for the committee election!

endpoint = 'http://trust-engine-dev.herokuapp.com/api/v1/delegations'
headers = {'x-trust-me': ')/6GrsL^bD%tC2EUR2n.x4^8r(=XbumMv@YfQL7)9PbF4zr8s9',
           'Accept': 'application/json'}

r = requests.get(endpoint, headers=headers)
response = r.json()


G = nx.DiGraph()
for edge in response.get('delegations'):
    fromUserId = edge.get('fromUserId')
    toUserId = edge.get('toUserId')
    topicId = edge.get('topicId')
    edge_id = edge.get('id')
    G.add_edge(fromUserId, toUserId, id=edge_id, topic=topicId)

committee = elect_committee(G, 1)
print("Committee:")
print({k: len(v) for k, v in committee.items()})
print(committee)
draw(paint_graph(G, committee))
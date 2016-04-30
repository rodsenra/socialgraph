from flask import Flask, request, jsonify, Response
import requests
import networkx as nx
from nxpd import draw
from socialgraph.socialgraph import  elect_committee, paint_graph


app = Flask(__name__)


@app.route('/committee', methods=['POST'])
def compute_committee():

    mandatory_params = ('topic', 'member_limit', 'get_delegations', 'headers')
    if not set(mandatory_params).issubset(set(request.json.keys())):
        return Response('You have to specify all {0} in your request'.format(mandatory_params), status=400)

    topic = request.json['topic']
    member_limit = request.json["member_limit"]
    endpoint = request.json["get_delegations"]
    headers = request.json["headers"]

    r = requests.get(endpoint, headers=headers)
    if r.status_code != 200:
        return Response('Failed to access {endpoint} with error code {error} and msg: {msg}'.format(endpoint=endpoint,
                                                                                                    error=r.status_code,
                                                                                                    msg=r.text))
    response = r.json()

    # Build graph
    G = nx.DiGraph()
    for edge in response.get('delegations'):
        fromUserId = edge.get('fromUserId')
        toUserId = edge.get('toUserId')
        topicId = edge.get('topicId')
        edge_id = edge.get('id')
        print(topicId)
        if topicId != topic:
            continue
        G.add_edge(fromUserId, toUserId, id=edge_id, topic=topicId)

    if len(G) == 0:
        msg = 'The topic {topic} was not found in the graph retreived from {endpoint}'
        return Response(msg.format(topic=topic, endpoint=endpoint))

    committee = elect_committee(G, int(member_limit))
    return jsonify(committee=committee)


if __name__ == "__main__":
    import sys
    try:
        host = sys.argv[1]
    except IndexError as e:
        print "Server expects : server_IP port"

    port = int(sys.argv[2])
    app.run(host=host, port=port)

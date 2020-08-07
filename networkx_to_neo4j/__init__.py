from neo4j import GraphDatabase
import neo4j
import numpy as np
import networkx as nx
import progressbar


def write_networkx_to_neo4j(tx:neo4j.Session, graph:nx.DiGraph, label_field:str = "labels", type_field:str = "labels", graph_uid:str = None):
    '''
    :param tx: neo4j Session object
    :param graph: a networkx DiGraph object, containing the graph which should be uploaded
    :param label_field: name of the attribute of networkx nodes, which should be taken as the node label in neo4j
    :param type_field: name of the attribute of networkx edges, which should be taken as the edge type in ne4j
    :param graph_uid: a uniqe identifier which will be added as attribute graph_uid to each node and edge
    '''
    if graph_uid is None:
        graph_uid = int(time.time())

    i=0
    with progressbar.ProgressBar(max_value=len(graph.nodes)+len(graph.edges)) as bar:
        for node in graph.nodes:
            i += 1
            bar.update(i)
            __add_node_to_neo4j(tx, node, graph.nodes[node], graph_uid, label_field)

        for u,v,c in graph.edges.data():
            i += 1
            bar.update(i)
            if isinstance(u, np.int64):
                u = int(u)
            if isinstance(v, np.int64):
                v = int(v)
            __add_edge_to_neo4j(tx, (u,v), c, graph_uid, type_field)



def __add_node_to_neo4j(tx:neo4j.Session, node, attr, graph_uid, label_field):
    if "contraction" in attr.keys():
        attr.pop("contraction")

    create_str = ["MERGE (n:{label_field}{{graph_uid:$graph_uid, node_id:$node_id}})".format(label_field=attr.get(label_field, "DUMMY_LABEL"))]
    create_str = create_str + ["SET n.{key}=${key}".format(key=key) for key in attr.keys() if key != label_field]
    create_str = create_str +["SET n.node_id=$node_id"]
    attr["graph_uid"] = graph_uid
    attr["node_id"] = node
    tx.run("   ".join(create_str), **attr)

def __add_edge_to_neo4j(tx:neo4j.Session, edge, attr, graph_uid, type_field):
    if "node_id" in attr.keys():
        attr.pop("node_id")

    create_str = ["MATCH (n1{graph_uid:$graph_uid, node_id:$n1}), (n2{graph_uid:$graph_uid, node_id:$n2})"]
    create_str = create_str + ["CREATE (n1)-[e:{type_field}{{graph_uid:$graph_uid}}]->(n2)".format(type_field=attr.get(type_field, "DUMMY_TYPE"))]
    create_str = create_str + ["SET e.{key}=${key}".format(key=key) for key in attr.keys() if key != type_field]
    attr["graph_uid"] = graph_uid
    attr["n1"] = edge[0]
    attr["n2"] = edge[1]
    tx.run("   ".join(create_str), **attr)



if __name__ == "__main__":
    graph = nx.gn_graph(20)
    nx.set_node_attributes(graph,"labels", "MY_NODE")
    nx.set_edge_attributes(graph,"types", "MY_EDGE")
    driver = GraphDatabase.driver(uri="bolt://xxx.xxx.xxx.xxx:7687", auth=("neo4j_user", "neo4j_pw"), max_connection_lifetime = 1000)
        with driver.session() as session:
            session.write_transaction(write_networkx_to_neo4j, graph, label_field="labels", type_field="types", graph_uid="I'm a uniqe graph")









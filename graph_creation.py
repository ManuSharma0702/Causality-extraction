import networkx as nx
import matplotlib.pyplot as plt
import json
json_data = {
  "Relations": [
    {
      "Entity1": "LQTS-3",
      "Entity2": "Na(v)1.5 cardiac sodium channel",
      "Relation": "Association",
      "Explanation": "The LQTS-3 mutation was identified in the transmembrane segment 6 of domain IV of the Na(v)1.5 cardiac sodium channel, indicating an association between the two entities."
    },
    {
      "Entity1": "Na(v)1.5 cardiac sodium channel",
      "Entity2": "V1764M",
      "Relation": "Association",
      "Explanation": "The electrophysiological profile of the Na(v)1.5 cardiac sodium channel was similar to that of the neighboring V1764M mutant, indicating an association between the two entities."      
    },
    {
      "Entity1": "Na(v)1.5 cardiac sodium channel",
      "Entity2": "I1762A",
      "Relation": "Association",
      "Explanation": "The electrophysiological profile of the Na(v)1.5 cardiac sodium channel was compared to that of the neighboring I1762A mutant, indicating an association between the two entities."     
    },
    {
      "Entity1": "lidocaine",
      "Entity2": "ventricular tachycardia",
      "Relation": "Cotreatment",
      "Explanation": "The 2:1 atrioventricular block improved to 1:1 conduction only after intravenous lidocaine infusion, which controlled the ventricular tachycardia, indicating that lidocaine was used to treat ventricular tachycardia."
    },
    {
      "Entity1": "lidocaine",
      "Entity2": "tetrodotoxin-sensitive current",
      "Relation": "Conversion",
      "Explanation": "The expression of the mutant channel in tsA201 mammalian cells revealed a persistent tetrodotoxin-sensitive but lidocaine-resistant current, indicating that lidocaine converted the channel to a resistant state."
    },
    {
      "Entity1": "methionine (ATG)",
      "Entity2": "V1763M",
      "Relation": "Conversion",
      "Explanation": "The substitution of valine (GTG) to methionine (ATG) resulted in the V1763M channel dysfunction, indicating that methionine was converted from valine."
    },
    {
      "Entity1": "patient",
      "Entity2": "fetal bradycardia",
      "Relation": "Association",
      "Explanation": "The patient had fetal bradycardia, indicating an association between the two entities."
    }
  ]
}

from pyvis.network import Network


def graph_creation(json_data):
    G = nx.DiGraph()

    # Add nodes and edges with relations
    for relation in json_data["Relations"]:
        entity1 = relation["Entity1"]
        entity2 = relation["Entity2"]
        relation_type = relation["Relation"]
        
        G.add_edge(entity1, entity2, label=relation_type)

    # Draw the graph
    pos = nx.spring_layout(G)  # Positioning of nodes

    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=3000, font_size=5, font_weight="bold", arrows=True)

    # Draw edge labels (relations)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=5)

    net = Network('900px', '900px')
    net.from_nx(G)												# The G is defined in Step 1.
    net.show('net.html', notebook=False)


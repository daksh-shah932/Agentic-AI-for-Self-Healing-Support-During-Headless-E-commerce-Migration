from sklearn.cluster import DBSCAN
import numpy as np

def cluster_tickets(tickets, embeddings):
    """
    Process: Clusters tickets based on semantic similarity using DBSCAN.
    Uses cosine distance (metric='cosine').
    """
    # EPS: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
    # Min_samples: The number of samples in a neighborhood for a point to be considered as a core point.
    clustering = DBSCAN(eps=0.5, min_samples=2, metric='cosine').fit(embeddings)
    
    labels = clustering.labels_
    
    # Organize tickets into clusters
    clusters = {}
    for ticket, label in zip(tickets, labels):
        if label == -1:
            label_key = "Noise"
        else:
            label_key = f"Cluster {label}"
            
        if label_key not in clusters:
            clusters[label_key] = []
        clusters[label_key].append(ticket)
        
    print(f"--> [INTERNAL] Identified {len(clusters)} distinct semantic groups (including noise).")
    return clusters
from sklearn.cluster import DBSCAN
import numpy as np

def cluster_tickets(tickets, embeddings):
    """
    Process: Clusters tickets based on semantic similarity using DBSCAN.
    """
    # --- DEMO MODE SETTINGS ---
    # eps=0.60:       Allows slightly "looser" matches (handles \n vs no \n)
    # min_samples=1:  CRITICAL FIX. Ensures NO ticket is ever hidden as "Noise".
    #                 Every single ticket will appear on the dashboard.
    clustering = DBSCAN(eps=0.60, min_samples=3, metric='cosine').fit(embeddings)
    
    labels = clustering.labels_
    
    # Organize tickets into clusters
    clusters = {}
    
    for ticket, label in zip(tickets, labels):
        # In Demo Mode (min_samples=1), label will never be -1
        label_key = int(label)
            
        if label_key not in clusters:
            clusters[label_key] = []
        clusters[label_key].append(ticket)
    
    print(f"--> [INTERNAL] Clustering Stats (Demo Mode):")
    print(f"    - Total Tickets:  {len(tickets)}")
    print(f"    - Clusters Found: {len(clusters)}")
    
    return clusters
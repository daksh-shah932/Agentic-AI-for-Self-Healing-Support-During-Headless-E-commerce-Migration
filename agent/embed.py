from sentence_transformers import SentenceTransformer

# Initialize model once to avoid reloading
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(tickets):
    """
    Process: Converts ticket messages to vector embeddings.
    """
    messages = [t['message'] for t in tickets]
    embeddings = model.encode(messages)
    
    print(f"--> [INTERNAL] Generated embeddings for {len(messages)} tickets.")
    return embeddings
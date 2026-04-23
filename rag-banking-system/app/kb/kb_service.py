from app.kb.token import validate_token

KB_DATA = {
    "home loan": "Interest rate is 8.5% for home loans."
}

def fetch_from_kb(token, query):
    if not validate_token(token):
        return "Invalid Token"
    
    for key in KB_DATA:
        if key in query.lower():
            return KB_DATA[key]
    
    return "No data found"
# app/utils/token_blacklist.py

# A simple in-memory blacklist (use Redis or DB in production)
BLACKLIST = set()

def add_token_to_blacklist(jti):
    BLACKLIST.add(jti)

def is_token_blacklisted(jti):
    return jti in BLACKLIST

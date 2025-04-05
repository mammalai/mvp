from posixpath import join as posixpath_join
from uuid import uuid4

def multi_urljoin(*parts):
    formatted_parts = []
    for part in parts:
        formatted_parts.append(part.rstrip('/').lstrip('/'))
    return posixpath_join(*formatted_parts)

def generate_id():
    return uuid4()

from requests import get, post, delete

print(get('http://localhost:5000/api/jobs').json())

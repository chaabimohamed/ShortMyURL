import requests

# post
res = requests.post('http://localhost:5000/users', json={"email":"ssd", "password":"sss"})
#res = requests.delete('http://localhost:5000/users/1')





# test
if res.ok:
    print(res)

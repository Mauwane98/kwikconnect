import requests

base='http://127.0.0.1:5000'

print('Register vendor...')
r = requests.post(base+'/api/v1/auth/register', json={'username':'vendor1','email':'vendor1@example.com','password':'password123','role':'vendor'})
print(r.status_code, r.text)

print('Register customer...')
r2 = requests.post(base+'/api/v1/auth/register', json={'username':'cust1','email':'cust1@example.com','password':'password123','role':'customer'})
print(r2.status_code, r2.text)

# login customer
print('Login customer...')
r3 = requests.post(base+'/api/v1/auth/login', json={'email':'cust1@example.com','password':'password123'})
print(r3.status_code, r3.text)

# login vendor
print('Login vendor...')
r4 = requests.post(base+'/api/v1/auth/login', json={'email':'vendor1@example.com','password':'password123'})
print(r4.status_code, r4.text)

if r3.status_code==200:
    token = r3.json().get('access_token')
    print('Customer token', token[:30]+'...')

if r4.status_code==200:
    vtoken = r4.json().get('access_token')
    print('Vendor token', vtoken[:30]+'...')


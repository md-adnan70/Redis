import redis

r = redis.Redis(host='localhost', port=6379, db=0) #Connect python to Redis server

try:
    if r.ping(): #Tests the connection
        print('Connected to Redis!')
except redis.ConnectionError:
    print('Redis connection failed!')


r.set('framework','FastAPI') #Stores a value in Redis

value = r.get('framework') #Retreives a value
print(f"Stored value for framework: {value.decode()}")  #Convert bytes to a readable string



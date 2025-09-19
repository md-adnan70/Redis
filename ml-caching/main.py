from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
import hashlib
import joblib
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] (line %(lineno)d - %(levelname)s - %(message)s)",
    datefmt="%d-%m-'%Y %H:%M:%S"
)


app = FastAPI()
logging.info('Initialized the FastAPI....')
print({redis.__version__})
redis_client = redis.Redis(host = 'localhost', port=6379, db=0)
logging.info("Initialized Redis Client")



model = joblib.load('model.joblib')

class IrisFlower(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float

    def to_list(self):
        return [
            self.SepalLengthCm,self.SepalWidthCm,self.PetalLengthCm,self.PetalWidthCm
        ]
    
    def cache_key(self):
        raw = json.dumps(self.model_dump(), sort_keys=True)
        return f"Predicted: {hashlib.sha256(raw.encode()).hexdigest()}"
    
@app.post('/predict')
async def predict(data: IrisFlower):
    key = data.cache_key()
    
    cached_result = redis_client.get(key)
    if cached_result:
        logging.info('Serving prediction from Cache!')
        return json.loads(cached_result)
    
    prediction = model.predict([data.to_list()])[0]
    result = {'prediction':int(prediction)}
    redis_client.set(key, json.dumps(result), ex=3600)
    return result
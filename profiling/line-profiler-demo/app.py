import time
from fastapi import FastAPI

app = FastAPI()

def computation(n:int):
    result = 0
    for i in range(n):
        result += (i*2)
    time.sleep(1)
    return result

@profile
def process_data(x: int):
    return computation(x)

@app.get('/profiling')
def profiling(a: int):
    return {'result':process_data(a)}


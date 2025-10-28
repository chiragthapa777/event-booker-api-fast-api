from fastapi import FastAPI
import asyncio
import time
import uvicorn

app = FastAPI()

@app.get("/")
async def hello_server():
    return {"hello":"world"}


@app.get("/async")
async def async_route():
    """
        result it can handle as much request no limitation
        concurrent request => time taken to resolve
        100 => 6s 
        300 => 6s
        500 => 6s
    """
    start = time.time()
    print(f"[ASYNC] Started at {start}")
    await asyncio.sleep(5)  # Simulates async I/O (non-blocking)
    end = time.time()
    print(f"[ASYNC] Finished at {end} | Duration: {end - start:.2f}s")
    return {"type": "async", "duration": end - start}

@app.get("/sync")
def sync_route():
    """
        result it can only 40 concurrent request
        concurrent request => time taken to resolve
        100 req => 11s (40 + 40 + 20)
        40 req => 6s
    """
    start = time.time()
    print(f"[SYNC] Started at {start}")
    time.sleep(5)  # Blocking sleep
    end = time.time()
    print(f"[SYNC] Finished at {end} | Duration: {end - start:.2f}s")
    return {"type": "sync", "duration": end - start}

# anti pattern X X X X
@app.get("/async-blocking")
async def async_blocking_route():
    """
        This will block the main thread
        and the main thread will not be able to serve other request
    """
    start = time.time()
    print(f"[ASYNC-BLOCKING] Started at {start}")
    # Simulate CPU-bound work that blocks the event loop
    for _ in range(1000000000):
        pass
    end = time.time()
    print(f"[ASYNC-BLOCKING] Finished at {end} | Duration: {end - start:.2f}s")
    return {"type": "async-blocking", "duration": end - start}

@app.get("/async-anti")
async def async_route():
    """
        it will block the main thread
    """
    start = time.time()
    print(f"[ASYNC] Started at {start}")
    await time.sleep(5)  # will block the main thread
    end = time.time()
    print(f"[ASYNC] Finished at {end} | Duration: {end - start:.2f}s")
    return {"type": "async", "duration": end - start}


@app.get("/sync-blocking")
def sync_blocking_route():
    """
        This will not block the main thread, the main thread will run this in thread pool
        and the main thread will be able to serve other request through single core context switching
        1 req = 8s
        2 req = 19s (concludes not truly parallel, thread is processed through context switching)
    """
    start = time.time()
    print(f"[SYNC-BLOCKING] Started at {start}")
    # Simulate CPU-bound work that blocks the event loop
    for _ in range(1000000000):
        pass
    end = time.time()
    print(f"[SYNC-BLOCKING] Finished at {end} | Duration: {end - start:.2f}s")
    return {"type": "async-blocking", "duration": end - start}


def blocking_work():
    start = time.time()
    print(f"[OFFLOAD-WORK] Started at {start}")
    for _ in range(1000000000):
        pass
    end = time.time()
    print(f"[OFFLOAD-WORK] Finished at {end} | Duration: {end - start:.2f}s")
    return end - start


@app.get("/async-offload")
async def async_offload_route():
    """
        This will not block the main thread, the main thread will run this in thread pool
        and the main thread will be able to serve other request through single core context switching
        1 req = 8s
        2 req = 19s (concludes not truly parallel, thread is processed through context switching)
    """
    duration = await asyncio.to_thread(blocking_work)
    return {"type": "async-offload", "duration": duration}


if __name__ == "__main__":
    uvicorn.run("async_test:app", workers=1) # to achieve true parallel work, increase workers, basically running multiple instance of the app

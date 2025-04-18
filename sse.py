import asyncio
from fastapi.responses import StreamingResponse

subscribers = set()


async def event_generator():
    queue = asyncio.Queue()
    subscribers.add(queue)
    try:
        while True:
            data = await queue.get()
            yield f"data: {data}\n\n"
    except asyncio.CancelledError:
        subscribers.remove(queue)


def broadcast_update(data: str):
    for queue in subscribers:
        queue.put_nowait(data)


def get_stream():
    return StreamingResponse(event_generator(), media_type="text/event-stream")

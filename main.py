import uvicorn
from fastapi import FastAPI, Path, Body
from typing import Optional
import uuid
from lib.recognition_streaming import RecognitionStreaming

app = FastAPI()


@app.get(
    '/',
    status_code=200
)
def root():
    return {'message': 'Hello World'}


@app.post(
    '/stream',
    status_code=200
)
def post_stream():
    stream_id = str(uuid.uuid4())
    return {
        'stream_id': stream_id
    }


@app.patch(
    '/stream/{stream_id}',
    status_code=202
)
def patch_stream(
    stream_id: str = Path(
        default='',
    ),
    stream_status: Optional[str] = Body(
        default='',
        description='start|stop'
    )
):
    recognition_streaming = RecognitionStreaming(stream_id)
    message = recognition_streaming.recognition_stream(stream_status)

    if message:
        return {
            'message': message
        }
    else:
        return {
            'message': 'Job Accepted'
        }


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)

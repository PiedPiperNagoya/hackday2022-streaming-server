import uvicorn
from fastapi import FastAPI, Path
import uuid
from .lib.recognition_streaming import RecognitionStreaming

app = FastAPI()


@app.get('/')
def root():
    return {'message': 'Hello World'}


@app.post('/stream')
def post_stream():
    stream_id = str(uuid.uuid4())
    return {
        'stream_id': stream_id
    }


@app.patch('/stream/{stream_id}')
def patch_stream(
        stream_id: str = Path(
            default='',
        )
):
    recognition_streaming = RecognitionStreaming(stream_id)
    recognition_streaming.recognition_stream()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

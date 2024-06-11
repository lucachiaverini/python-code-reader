import cv2, zxingcpp
import numpy as np
from fastapi import FastAPI, File
from pydantic import BaseModel
import logging
from enum import Enum

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

class BarcodeType(Enum):
    DATAMATRIX = "datamatrix"
    QRCODE = "qrcode"
    
class BarcodeResponse(BaseModel):
    type: BarcodeType = None
    code: str = None

@app.post("/api/decode")
async def read_root(file: bytes = File(...)):

    if not file:
        return BarcodeResponse()
    
    image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)

    barcodes = zxingcpp.read_barcodes(image)
    for barcode in barcodes:
        logger.info('Found barcode:'
            f'\n Text:    "{barcode.text}"'
            f'\n Format:   {barcode.format}'
            f'\n Content:  {barcode.content_type}'
            f'\n Position: {barcode.position}')
    if not barcodes:
        logger.warning("Could not find any barcode.")
        return BarcodeResponse()
    
    split = barcode.text.split(" ")

    logger.info(f"Split: {barcode.text.split()}")
    logger.info(f'Barcode format: {barcode.format}')

    if str(barcode.format) == 'BarcodeFormat.DataMatrix':
        return BarcodeResponse(type=BarcodeType.DATAMATRIX,code= split[0])

    return BarcodeResponse(type=BarcodeType.QRCODE,code = barcode.text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8443, ssl_keyfile="./cert/tls.key", ssl_certfile="./cert/tls.crt", lifespan="on")
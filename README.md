# Python barcode decoder

A simple microservice for decoding a QrCode or Datamatrix barcode.

## Installation

Navigate to the source code path.

Run the following commands:

- Create environment in the local path: `python -m venv ./env`
- Activate environment (Windows): `./env/Scripts/activate`
- Install libraries: `python -m pip install -r ./requirements.txt`

## Running the application

```bash
python ./main.py
```

## Calling the decode service

```bash
curl --location 'https://localhost:8443/api/decode' --form 'file=@"<local_path_of_file>"'
```
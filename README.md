# Notes API

## What the project does
A very small HTTP service written in Python. It stores short text notes in memory.

- `GET /` - service info
- `GET /healthz` - health check, returns 200
- `GET /notes` - list all notes
- `POST /notes` - add a note, body: `{"text": "my note"}`

## How to run it
```
./scripts/run.sh
```
Python 3 is needed. No extra packages are required.

## How to test it
```
./scripts/test.sh
```
It runs the tests and prints a line like `TESTS: 3/3`.

## Port
The service reads the port from the `PORT` environment variable. The default is `8080`.
```
PORT=9000 ./scripts/run.sh
```

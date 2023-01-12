# Settings

Define variables in config.py:

```
API_KEY
API_SECRET_KEY
API_BEARER_TOKEN
API_ACCESS_TOKEN
API_ACCESS_TOKEN_SECRET
```
	
# How to run:

Change directory with command:

```
cd src
```

To launch uvicorn run command:

```
uvicorn twitter_parser.main:app --reload
```

Then load docs page at

http://127.0.0.1:8000/
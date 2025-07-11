# setup
```bash
pip install -r requirements.txt
```

# run 
```bash 
uvicorn main:app --reload
```

# curl test requests
## saving
### positive sentiment
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text":"хороший запах"}' http://127.0.0.1:8000/reviews
```
`< HTTP/1.1 204 No Content`

### neutral sentiment
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text":"мне нравится"}' http://127.0.0.1:8000/reviews
```
`< HTTP/1.1 204 No Content`


### negative sentiment
```bash
curl -X POST -H "Content-Type: application/json" -d '{"text":"ненавижу запах"}' http://127.0.0.1:8000/reviews
```
`< HTTP/1.1 204 No Content`


## getting
### all review list
```bash
curl http://127.0.0.1:8000/reviews
```

### positive review list
```bash
 curl http://127.0.0.1:8000/reviews?sentiment=positive
 ```
```json
[{"id":1,"text":"хороший запах","sentiment":"positive","created_at":"2025-07-11T16:51:04.045347"},{"id":4,"text":"хороший запах","sentiment":"positive","created_at":"2025-07-11T17:03:25.102729"}]
```
### negative review list
 ```bash
 curl http://127.0.0.1:8000/reviews?sentiment=negative
 ```

### neutral review list
 ```bash
 curl http://127.0.0.1:8000/reviews?sentiment=neutral
```

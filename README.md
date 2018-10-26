# Health Assistant API

---

Here our API for Health Assistant.

## Checking connection
To check connection just ping __/connect/__ page. If everything is fine, you'll get next response: 
```js
{"connect_status": "OK"}
```

## Logging in
```js
get request: /login/{"username": "<username>", "password": "<password>"}
response: {"session_id": "<id>"}
```

## Getting Health Assistance Request
```js
get request: /start_health_test/{"session_id": "<id>"}
response: {"test_id": "<id>"}
```

## Health Testing Question Request
```js
get request: /health_test_get_question/{"session_id": "<id>", "test_id": "<id>", "quesion_number": <number>}
response: {"question": "<question>"}
```

## Health Testing Question Response
```js
get request: /health_test_post_answer/{"session_id": "<id>", "test_id": "<id>", "quesion_number": <number>, "response": <response>}
response: {"next_stage": "<next_question_number/goto_results>"}
```

## Health Testing Result
```js
get request: /health_test_results/{"session_id": "<id>", "test_id": "<id>"}
response: {"results": "<diagnosis>"}
```

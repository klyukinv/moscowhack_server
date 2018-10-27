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
response: {"session_id": "<session_id>"}
```

## Getting Health Assistance Request
```js
get request: /start_health_test/{"username": "<username>", "session_id": "<session_id>"}
response: {"test_id": "<test_id>"}
```

## Health Testing Question Request
```js
get request: /health_test_get_question/{"username": "<username>", "session_id": "<session_id>", "test_id": "<test_id>", "quesion_number": <number>}
response: {"question": "<question>"}
```

## Health Testing Question Response
```js
get request: /health_test_post_answer/{"username": "<username>", "session_id": "<session_id>", "test_id": "<test_id>", "quesion_number": <number>, "response": <response>}
response: {"next_stage": "<next_question_number/goto_results>"}
```

## Health Testing Result
```js
get request: /health_test_results/{"username": "<username>", "session_id": "<session_id>", "test_id": "<test_id>"}
response: {"results": "<diagnosis>"}
```

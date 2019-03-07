# timing-asgi middleware example

This repository contains a tiny [starlette](https://www.starlette.io) ASGI
application, to demonstrate how the [timing-asgi](https://github.com/steinnes/timing-asgi)
middleware can be used to automatically instrument routes in an ASGI application
and emit timing metrics, for example to [datadog](https://www.datadog.com) via
statsd.

## setup

```
$ make run
...
Successfully installed alog-0.9.13 certifi-2018.11.29 chardet-3.0.4 click-7.0 datadog-0.27.0 decorator-4.3.2 h11-0.8.1 httptools-0.0.13 idna-2.8 requests-2.21.0 starlette-0.11.3 timing-asgi-0.1.0rc1 urllib3-1.24.1 uvicorn-0.5.1 uvloop-0.12.1 websockets-7.0
venv/bin/python app.py
INFO: Started server process [24774]
INFO: Waiting for application startup.
2019-03-07 09:40:24 INFO  [timing_asgi.middleware:44] ASGI scope of type lifespan is not supported yet
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO: ('127.0.0.1', 54016) - "GET / HTTP/1.1" 200
```

## see in action

If you're like me, you'd like to see something being emitted, which is easy to
do with netcat:

Keep the server running from the step above, then open two shells.

In the first run:

```
$ nc -ul 8125
```

In the second run:

```
$ curl http://127.0.0.1:8000/
```

If for some reason your app server isn't listening on 127.0.0.1:8000 replace
the value above with the one reported by uvicorn when running the app initially.

This curl command when successful will cause the `nc` shell to print out the
raw statsd data it collected on port 8125:
```
myapp.__main__.homepage:0.001255035400390625|ms|#http_status:200,http_method:GET,time:wall,app_version:myapp.__main__.homepage:0.0010529999999999706|ms|#http_status:200,http_method:GET,time:cpu,app_version:
```

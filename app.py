import os
import uvicorn

from datadog import initialize, statsd
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from timing_asgi import TimingMiddleware, TimingClient
from timing_asgi.integrations import StarletteScopeToName


initialize({'api_key': 'datadog api key', 'app_key': 'datadog app key'})

app = Starlette()


class StatsdClient(TimingClient):
    def __init__(self, datadog_client, tags=None):
        if tags is None:
            tags = []
        self.tags = tags
        self.datadog_client = datadog_client

    def timing(self, metric_name, timing, tags):
        self.datadog_client.timing(metric_name, timing, tags + self.tags)


@app.route("/")
def homepage(request):
    return PlainTextResponse("hello world")

app.add_middleware(
    TimingMiddleware,
    client=StatsdClient(
        datadog_client=statsd,
        tags=['app_version:'.format(os.environ.get('GITHASH'), 'unknown')],
    ),
    metric_namer=StarletteScopeToName(
        prefix="myapp",
        starlette_app=app
    )
)

if __name__ == "__main__":
    uvicorn.run(app)

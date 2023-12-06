from flask import Flask, render_template, request

from jaeger_client import Config
from flask_opentracing import FlaskTracing
from prometheus_flask_exporter import PrometheusMetrics

import traceback
import logging

app = Flask(__name__)

# prometheus https://pypi.org/project/prometheus-flask-exporter/
metrics = PrometheusMetrics(app, group_by="endpoint")
metrics.info('app_info', 'Application info', version='1.0.3')
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

# jaeger https://github.com/opentracing-contrib/python-flask
config = Config(config={'sampler': {'type': 'const', 'param': 1},
                        'logging': True},
                service_name="service_frontend"
                )

tracer = config.initialize_tracer()
tracing = FlaskTracing(tracer, True, app)

@app.route("/")
def homepage():
    return render_template("main.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/ex")
def ex():
    logging.error("demo-error-log")
    with tracer.start_span('my-api'):
        return render_template("testx.html")

if __name__ == "__main__":
    app.run()

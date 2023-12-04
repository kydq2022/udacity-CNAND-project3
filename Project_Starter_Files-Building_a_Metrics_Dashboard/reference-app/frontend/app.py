from flask import Flask, render_template, request
from prometheus_flask_exporter import PrometheusMetrics
from jaeger_client import Config
from flask_opentracing import FlaskTracing


app = Flask(__name__)

# prometheus https://pypi.org/project/prometheus-flask-exporter/
metrics = PrometheusMetrics(app)
metrics.info('project3_frontend', 'project3 frontend', version='1.0.3')
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

# jaeger https://github.com/opentracing-contrib/python-flask
config = Config(config={'sampler': {'type': 'const', 'param': 1},
                        'logging': True},
                service_name="project3_fe")
tracer = config.initialize_tracer()
tracing = FlaskTracing(tracer)

@app.route("/")
@tracing.trace()
def homepage():
    return render_template("main.html")

@app.route("/test")
@tracing.trace()
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run()

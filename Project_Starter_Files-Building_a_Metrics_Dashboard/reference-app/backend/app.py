from flask import Flask, request, jsonify

from flask_pymongo import PyMongo
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from prometheus_flask_exporter import PrometheusMetrics
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

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
metrics = GunicornInternalPrometheusMetrics(app)

# jaeger https://github.com/opentracing-contrib/python-flask
config = Config(config={'sampler': {'type': 'const', 'param': 1},
                        'logging': True},
                service_name="service_backend",
                metrics_factory=PrometheusMetricsFactory(service_name_label="service_backend")
                )

tracer = config.initialize_tracer()
tracing = FlaskTracing(tracer, True, app)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

@app.route("/")
def homepage():
    return "kydq2022 project3 222 333"


@app.route("/api")
def my_api():
    answer = "kydq2022 project 3 api 333"
    return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
def add_star():
    star = mongo.db.stars
    name = request.json["name"]
    distance = request.json["distance"]
    star_id = star.insert({"name": name, "distance": distance})
    new_star = star.find_one({"_id": star_id})
    output = {"name": new_star["name"], "distance": new_star["distance"]}
    return jsonify({"result": output})


if __name__ == "__main__":
    app.run()

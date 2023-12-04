from flask import Flask, request, jsonify

from flask_pymongo import PyMongo
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info("project3_backend", "project3-backend", version="1.0.3")
endpoint_counter = metrics.counter(
    'by_endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)

config = Config(config={'sampler': {'type': 'const', 'param': 1},
                        'logging': True},
                service_name="project3_backend")

tracer = config.initialize_tracer()

tracing = FlaskTracing(tracer)


app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

@app.route("/")
@tracing.trace()
@endpoint_counter
def homepage():
    return "kydq2022 project3 222"


@app.route("/api")
@tracing.trace()
@endpoint_counter
def my_api():
    answer = "kydq2022 project 3 api"
    return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
@tracing.trace()
@endpoint_counter
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

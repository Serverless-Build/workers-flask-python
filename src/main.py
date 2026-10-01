from flask import Blueprint, Flask, request
from workers import wsgi

app = Flask(__name__)
api = Blueprint("api", __name__)


@api.get("/")
def index():
    return {"framework": "Flask", "adapter": "Workers WSGI", "routes": ["/health", "/quote?quantity=3&unit_price_cents=250"]}


@api.get("/health")
def health():
    return {"status": "ok", "marker": "SERVERLESS_BUILD_FLASK_PYTHON_V1"}


@api.get("/quote")
def quote():
    values = {}
    errors = {}
    for name, maximum in (("quantity", 100), ("unit_price_cents", 1000000)):
        raw = request.args.getlist(name)
        if len(raw) != 1 or not raw[0].isascii() or not raw[0].isdigit() or len(raw[0]) > 7:
            errors[name] = "Supply exactly one integer value."
        else:
            value = int(raw[0])
            if not 1 <= value <= maximum:
                errors[name] = f"Must be between 1 and {maximum}."
            else:
                values[name] = value
    if errors:
        return {"error": "Invalid quote", "fields": errors}, 400
    return {**values, "total_cents": values["quantity"] * values["unit_price_cents"], "currency": "USD"}


@app.after_request
def headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.errorhandler(404)
@app.errorhandler(405)
def http_error(error):
    response = error.get_response()
    response.data = app.json.dumps({"error": error.name})
    response.content_type = "application/json"
    return response


app.register_blueprint(api)
Default = wsgi.entrypoint(app)

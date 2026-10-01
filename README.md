# Flask on Workers

Run Flask through Python Workers’ native WSGI adapter, with blueprint routing, bounded input validation, and structured JSON responses.

## Run locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Node.js 22 or later.

```sh
npm ci
uv sync --locked
uv run pywrangler dev --config wrangler.jsonc
```

## Check and deploy

```sh
uv run pywrangler deploy --config wrangler.jsonc
```

The configuration is portable: it contains no account ID, resource ID, or maintainer custom domain. Log in with Wrangler and select your own account before deploying. Generated dependencies and build outputs stay out of source control.

## Try the example

GET /health checks liveness. GET /quote?quantity=3&unit_price_cents=250 returns a 750-cent quote. Try quantity=0, 101, a decimal, duplicate values, or missing inputs to see HTTP 400 validation errors. Both values are bounded integers (quantity 1–100; unit price 1–1000000).

Flask uses a real Blueprint and the built-in Workers WSGI adapter. No Flask development server or socket listener runs in the Worker.

## Pattern and live demo

- [Pattern page](https://serverless.build/patterns/flask-workers)
- [Live deployment](https://workers-flask-python.dwarven.workers.dev)

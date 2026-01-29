import os
from flask import Flask, jsonify, send_from_directory
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import AzureError

app = Flask(__name__)


def _get_subscription_id():
    return os.environ.get("AZURE_SUBSCRIPTION_ID") or os.environ.get("SUBSCRIPTION_ID")


def _get_resources(subscription_id: str):
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=True)
    client = ResourceManagementClient(credential, subscription_id)
    # limit to first 200 resources for quick rendering
    return [
        {
            "id": r.id,
            "name": r.name,
            "type": r.type,
            "location": r.location,
            "kind": getattr(r, "kind", None),
        }
        for r in client.resources.list(top=200)
    ]


@app.route("/api/resources")
def resources():
    subscription_id = _get_subscription_id()
    if not subscription_id:
        return (
            jsonify(
                {
                    "error": "AZURE_SUBSCRIPTION_ID is not set. Configure the app setting so the managed identity knows which subscription to read."
                }
            ),
            500,
        )

    try:
        data = _get_resources(subscription_id)
        return jsonify({"subscriptionId": subscription_id, "items": data})
    except AzureError as exc:
        return (
            jsonify(
                {
                    "error": "Failed to query Azure resources. Ensure the Web App has a managed identity with Reader access on the subscription.",
                    "details": str(exc),
                }
            ),
            500,
        )
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": "Unexpected error", "details": str(exc)}), 500


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))

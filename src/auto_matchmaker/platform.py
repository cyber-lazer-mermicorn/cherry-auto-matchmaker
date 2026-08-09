"""
Auto Matchmaker — Platform Integration
========================================
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "mermicorn-client"))

from mermicorn_client import MermicornClient


def get_client() -> MermicornClient:
    return MermicornClient(
        api_url=os.environ.get("MERMICORN_API_URL", "http://localhost:8000"),
        api_key=os.environ.get("MERMICORN_API_KEY", ""),
    )


def sync_vehicles(vehicles: list[dict]) -> dict:
    """Sync vehicle inventory to central platform."""
    client = get_client()
    results = []
    for v in vehicles:
        result = client.vehicles.add(
            year=v["year"], make=v["make"], model=v["model"],
            price=v["price"], mileage=v.get("mileage", 0),
        )
        results.append(result)
    return {"synced": len(results), "results": results}

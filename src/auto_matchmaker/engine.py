"""Cherry Auto Matchmaker — Vehicle Research & Buyer Matching Engine."""

from __future__ import annotations
import hashlib, json, time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Vehicle:
    year: int
    make: str
    model: str
    price: float
    mileage: int
    condition: str = ""
    tags: list[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return f"{self.year} {self.make} {self.model}"

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "price": self.price, "mileage": self.mileage,
                "condition": self.condition, "tags": self.tags}


class AutoMatchEngine:
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.vehicles: list[Vehicle] = []

    def add_vehicle(self, year: int, make: str, model: str, price: float, mileage: int, **kw) -> Vehicle:
        v = Vehicle(year=year, make=make, model=model, price=price, mileage=mileage, **kw)
        self.vehicles.append(v)
        return v

    def match(self, max_price: float = 999999, max_mileage: int = 999999) -> list[Vehicle]:
        return [v for v in self.vehicles if v.price <= max_price and v.mileage <= max_mileage]

    def export(self) -> str:
        path = self.output_dir / "vehicles.json"
        path.write_text(json.dumps([v.to_dict() for v in self.vehicles], indent=2))
        return str(path)

    def get_stats(self) -> dict[str, Any]:
        return {"total": len(self.vehicles), "avg_price": sum(v.price for v in self.vehicles) / max(len(self.vehicles), 1)}

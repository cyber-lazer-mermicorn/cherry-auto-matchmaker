"""
Vehicle Vision — See Cars, Assess Condition
===========================================
Photo-based vehicle identification and assessment.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mermicorn-commerce-ai" / "src"))
from commerce_ai.vision import MermicornVision, VisionResult


class VehicleVision:
    """
    Vision-powered vehicle analysis.
    
    See a car → Identify it → Assess condition → Value it
    """
    
    def __init__(self, api_key: str | None = None):
        self.vision = MermicornVision(api_key=api_key)
    
    def identify_from_photo(self, image_path: str) -> VisionResult:
        """Identify a vehicle from a photo."""
        return self.vision.analyze_image(image_path, task="identify")
    
    def assess_from_photo(self, image_path: str) -> VisionResult:
        """Assess vehicle condition from photos."""
        prompt = """Analyze this vehicle image for condition assessment.

Identify:
- Make, model, year (if possible)
- Body condition (paint, dents, scratches)
- Tire condition
- Interior visible condition
- Modifications visible
- Overall condition rating

Provide JSON with:
- vehicle_identification: {make, model, year, color, body_style}
- exterior_condition: {rating: 1-10, notes, defects}
- visible_modifications: list
- condition_overall: excellent/good/fair/poor
- condition_score: 1-100
- estimated_mileage_range: {low, high}
- confidence: 0-1
- reasoning: explanation"""
        
        return self.vision.analyze_image(image_path, task="grade")
    
    def compare_vehicles(self, image1_path: str, image2_path: str) -> VisionResult:
        """Compare two vehicles."""
        return self.vision.compare_images(image1_path, image2_path)
    
    def get_stats(self) -> dict[str, Any]:
        return {"vision_stats": self.vision.get_stats()}

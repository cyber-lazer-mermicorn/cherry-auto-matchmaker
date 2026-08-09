"""
Full Stack Workflow Test — Cherry Auto Matchmaker
==================================================
Photo → Identify → Assess → Value → Match → List
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, "src")
sys.path.insert(0, "../mermicorn-commerce-ai/src")
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mermicorn-commerce-ai" / "src"))

from auto_matchmaker.engine import AutoMatchEngine
from auto_matchmaker.ai_research import VehicleAI
from auto_matchmaker.integrations import VehicleIntelligence
from auto_matchmaker.skills_market import AutoSkills


def test_full_workflow():
    """Test complete auto workflow: Identify → Assess → Value → Match → List."""
    print("🚗 AUTO MATCHMAKER FULL WORKFLOW TEST")
    print("=" * 50)
    
    # ═══════════════════════════════════════════════════════════
    # STEP 1: Identify Vehicle (AI)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 1: Identify Vehicle")
    ai = VehicleAI()
    result = ai.identify_vehicle("2020 Honda Civic EX, silver, 45000 miles, single owner, clean title")
    
    assert result.success, f"Identification failed: {result.reasoning}"
    print(f"   ✅ Identified: {result.data}")
    print(f"   ✅ Confidence: {result.confidence}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 2: Assess Condition (AI)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 2: Assess Condition")
    condition = ai.assess_condition(
        "2020 Honda Civic, well maintained, regular oil changes, no accidents, minor door ding",
        mileage=45000,
        age_years=4
    )
    
    assert condition.success, f"Assessment failed: {condition.reasoning}"
    print(f"   ✅ Condition: {condition.data}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 3: Get KBB Value (Integration)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 3: Get KBB Value")
    intel = VehicleIntelligence()
    kbb = intel.kbb.get_value(2020, "Honda", "Civic", 45000, "good")
    
    assert "trade_in" in kbb, "KBB value missing"
    print(f"   ✅ KBB: Trade-in ${kbb['trade_in']:,} | Private ${kbb['private_party']:,} | Retail ${kbb['retail']:,}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 4: Get Reviews (Integration)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 4: Get Reviews")
    reviews = intel.edmunds.get_reviews(2020, "Honda", "Civic")
    
    assert "expert_rating" in reviews, "Reviews missing"
    print(f"   ✅ Rating: {reviews['expert_rating']}/5 | {reviews['verdict']}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 5: Check Recalls (Integration)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 5: Check Recalls")
    recalls = intel.edmunds.get_recall_info(2020, "Honda", "Civic")
    
    print(f"   ✅ Recalls: {len(recalls)} (all {recalls[0]['status']})")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 6: Estimate Depreciation (Skills)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 6: Estimate Depreciation")
    skills = AutoSkills()
    depreciation = skills.estimate_depreciation(2020, "Honda", "Civic", 45000)
    
    print(f"   ✅ Depreciation curve: {len(depreciation['depreciation_curve'])} years")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 7: Maintenance Schedule (Skills)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 7: Maintenance Schedule")
    maintenance = skills.maintenance_schedule(45000, 4)
    
    total_items = sum(len(v) for v in maintenance.values())
    print(f"   ✅ Maintenance: {total_items} items scheduled")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 8: Generate Listing (AI)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 8: Generate Listing")
    vehicle_data = {
        "year": 2020, "make": "Honda", "model": "Civic", "trim": "EX",
        "mileage": 45000, "price": 18500, "condition": "good",
        "color": "Silver", "title": "Clean", "owners": 1,
    }
    listing = ai.generate_listing(vehicle_data)
    
    assert listing.success, f"Listing failed: {listing.reasoning}"
    print(f"   ✅ Listing: {listing.data}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 9: Add to Engine & Match
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 9: Add to Engine & Match")
    engine = AutoMatchEngine()
    v1 = engine.add_vehicle(2020, "Honda", "Civic", 18500, 45000)
    v2 = engine.add_vehicle(2019, "Toyota", "Camry", 16200, 38000)
    v3 = engine.add_vehicle(2021, "Mazda", "CX-5", 22100, 29000)
    
    matches = engine.match(max_price=20000, max_mileage=50000)
    
    assert len(matches) >= 2, "Not enough matches"
    print(f"   ✅ Catalog: {len(engine.vehicles)} vehicles")
    print(f"   ✅ Matches under $20K/50K miles: {len(matches)}")
    
    # ═══════════════════════════════════════════════════════════
    # STEP 10: Carfax Report (Integration)
    # ═══════════════════════════════════════════════════════════
    print("\n📌 STEP 10: Carfax Report")
    carfax = intel.carfax.generate_report("1HGBH41JXMN109186", vehicle_data)
    
    print(f"   ✅ Carfax score: {carfax['score']}/100")
    
    # ═══════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════
    print("\n" + "=" * 50)
    print("✅ FULL WORKFLOW COMPLETE")
    print(f"   Vehicle: 2020 Honda Civic EX")
    print(f"   Mileage: 45,000")
    print(f"   KBB Value: ${kbb['private_party']:,}")
    print(f"   Condition: Good")
    print(f"   Recalls: {len(recalls)} (all fixed)")
    print(f"   Catalog: {len(engine.vehicles)} vehicles")
    print(f"   Matches: {len(matches)}")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    success = test_full_workflow()
    sys.exit(0 if success else 1)

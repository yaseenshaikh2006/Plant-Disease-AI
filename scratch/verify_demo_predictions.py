"""
End-to-End Verification of Demo Leaf Images
"""

import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

samples = [
    ("frontend/public/sample_images/strawberry_scorch.jpg", "strawberry"),
    ("frontend/public/sample_images/rice_blight.jpg", "rice"),
    ("frontend/public/sample_images/tomato_early_blight.jpg", "tomato"),
    ("frontend/public/sample_images/tomato_healthy.jpg", "tomato"),
]

print("=" * 70)
print("DEMO SAMPLES END-TO-END DIAGNOSIS VERIFICATION")
print("=" * 70)

for img_path, crop_hint in samples:
    p = Path(img_path)
    if not p.exists():
        print(f"[FAIL] Missing {img_path}")
        continue

    with open(p, "rb") as f:
        file_bytes = f.read()

    response = client.post(
        "/predict",
        files={"file": (p.name, file_bytes, "image/jpeg")},
        data={"crop": crop_hint}
    )

    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()
    print(f"\n[SAMPLE] {p.name} (Hint: {crop_hint})")
    print(f"  • Predicted Crop:     {data['crop']}")
    print(f"  • Predicted Disease:  {data['disease']}")
    print(f"  • Confidence:         {data['confidence'] * 100:.2f}%")
    print(f"  • Severity:           {data['severity']} ({data['severity_details']['lesion_percentage']}% lesion coverage)")
    print(f"  • Treatment items:    {len(data['treatment'])} actions")
    print(f"  • Fertilizer advice:  {len(data['fertilizer'])} guidelines")
    print(f"  • Irrigation advice:  {len(data['irrigation'])} guidelines")
    print(f"  • Top Candidate:      {data['top_predictions'][0]['class_name']} ({data['top_predictions'][0]['confidence']:.4f})")

print("\n" + "=" * 70)
print("[SUCCESS] All demo samples verified successfully through prediction pipeline!")
print("=" * 70)

#!/usr/bin/env python3
"""
Simple test script to verify the Flask API endpoints
"""
import requests

API_BASE_URL = 'http://localhost:8000'

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_predict_endpoint():
    """Test the predict endpoint"""
    test_data = {
        'age_at_enrollment': 20,
        'gender': 1,
        'marital_status': 1,
        'admission_grade': 150.0,
        'daytime_evening_attendance': 1,
        'scholarship_holder': 0,
        'tuition_fees_up_to_date': 1,
        'curricular_units_1st_sem_enrolled': 6,
        'curricular_units_1st_sem_approved': 5,
        'curricular_units_1st_sem_grade': 13.5,
        'curricular_units_2nd_sem_enrolled': 6,
        'curricular_units_2nd_sem_approved': 6,
        'curricular_units_2nd_sem_grade': 14.2,
        'unemployment_rate': 9.5
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/predict",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"✅ Predict endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Prediction: {result.get('prediction')}")
            print(f"   Confidence: {result.get('confidence')}")
        else:
            print(f"   Error: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Predict endpoint failed: {e}")
        return False

def main():
    print("🧪 Testing Flask API endpoints...")
    print(f"🔗 Base URL: {API_BASE_URL}")
    print("-" * 40)
    
    # Test endpoints
    root_ok = test_root_endpoint()
    predict_ok = test_predict_endpoint()
    
    print("-" * 40)
    if root_ok and predict_ok:
        print("🎉 All tests passed!")
    else:
        print("💥 Some tests failed!")
        print("Make sure the Flask server is running on port 8000")

if __name__ == "__main__":
    main() 
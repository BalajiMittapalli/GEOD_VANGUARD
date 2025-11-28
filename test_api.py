import requests
import json
from datetime import datetime

# API endpoint
BASE_URL = "http://localhost:8000"

def test_analytics_api():
    """
    Test the financial analytics API with sample data
    """
    # Test data
    test_request = {
        "ticker": "MSFT",
        "start_date": "2020-01-01",
        "end_date": "2024-12-31"
    }
    
    print("Testing Financial Analytics API...")
    print(f"Request: {json.dumps(test_request, indent=2)}")
    
    try:
        # Make API call
        response = requests.post(f"{BASE_URL}/analytics/run", json=test_request)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ API Response Successful!")
            print(f"Ticker: {result['ticker']}")
            print(f"Max Drawdown: {result['max_drawdown']:.4f}")
            print(f"Beta: {result['beta']:.4f}")
            print(f"Unlevered Beta: {result['unlevered_beta']:.4f}")
            print(f"Optimal WACC: {result['optimal_wacc']:.4f}")
            print(f"Optimal Debt Ratio: {result['optimal_debt_ratio']:.2%}")
            print(f"Monthly Returns Count: {len(result['monthly_return'])}")
            print(f"WACC Curve Points: {len(result['wacc_curve'])}")
            
            # Show first few WACC curve points
            print("\nSample WACC Curve (first 5 points):")
            for i, point in enumerate(result['wacc_curve'][:5]):
                print(f"  Debt Ratio: {point['debt_ratio']:.1%}, WACC: {point['wacc']:.4f}")
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running on localhost:8000")
        print("Run: python financial_analytics_api.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_health_endpoint():
    """
    Test the health check endpoint
    """
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")

if __name__ == "__main__":
    print("=" * 50)
    print("Financial Analytics API Test")
    print("=" * 50)
    
    # Test health endpoint
    test_health_endpoint()
    print()
    
    # Test main analytics endpoint
    test_analytics_api()
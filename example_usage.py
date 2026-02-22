"""
Example usage of the LLM Evaluator API Layer 1.

This script demonstrates how to use the Domain Selection, 
Dynamic Rubric Builder, and Weight Configuration features.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def print_response(title: str, response: requests.Response):
    """Helper to print API responses."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    if response.status_code < 400:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")


def example_domain_operations():
    """Example: Domain Selection operations."""
    print("\n" + "="*60)
    print("DOMAIN SELECTION EXAMPLES")
    print("="*60)
    
    # Get all domains
    response = requests.get(f"{BASE_URL}/domains")
    print_response("Get All Domains", response)
    
    # Get domains by category
    response = requests.get(f"{BASE_URL}/domains?category=coding")
    print_response("Get Domains by Category (coding)", response)
    
    # Create a new custom domain
    new_domain = {
        "name": "Machine Learning",
        "category": "technical",
        "description": "Evaluation domain for ML model explanations and code",
        "metadata": {
            "frameworks": ["pytorch", "tensorflow", "sklearn"]
        }
    }
    response = requests.post(f"{BASE_URL}/domains", json=new_domain)
    print_response("Create New Domain", response)
    
    if response.status_code == 201:
        domain_id = response.json()["id"]
        
        # Get specific domain
        response = requests.get(f"{BASE_URL}/domains/{domain_id}")
        print_response(f"Get Domain by ID ({domain_id})", response)


def example_rubric_operations():
    """Example: Dynamic Rubric Builder operations."""
    print("\n" + "="*60)
    print("DYNAMIC RUBRIC BUILDER EXAMPLES")
    print("="*60)
    
    # Get all rubrics
    response = requests.get(f"{BASE_URL}/rubrics")
    print_response("Get All Rubrics", response)
    
    # Get rubrics by domain
    response = requests.get(f"{BASE_URL}/rubrics?domain_id=domain_coding")
    print_response("Get Rubrics by Domain (coding)", response)
    
    # Get available rubric types
    response = requests.get(f"{BASE_URL}/rubrics/types/list")
    print_response("Get Available Rubric Types", response)
    
    # Create a custom rubric
    custom_rubric = {
        "name": "Mathematical Problem Solving",
        "rubric_type": "mathematical_correctness",
        "domain_id": "domain_math",
        "evaluation_dimension": "response_quality",
        "description": "Evaluates mathematical problem-solving accuracy",
        "criteria": [
            {
                "name": "Solution Correctness",
                "description": "The solution must be mathematically correct",
                "weight": 0.5,
                "evaluation_guidelines": [
                    "Verify calculations",
                    "Check formula application",
                    "Validate final answer"
                ]
            },
            {
                "name": "Solution Method",
                "description": "The method used should be appropriate",
                "weight": 0.3,
                "evaluation_guidelines": [
                    "Check if method is efficient",
                    "Verify step-by-step approach"
                ]
            },
            {
                "name": "Explanation Quality",
                "description": "The explanation should be clear and comprehensive",
                "weight": 0.2,
                "evaluation_guidelines": [
                    "Check clarity of explanation",
                    "Verify completeness"
                ]
            }
        ],
        "scoring_scale": {
            "min_score": 0.0,
            "max_score": 10.0,
            "step": 0.1
        },
        "instructions": "Evaluate mathematical solutions based on correctness, method, and explanation.",
        "metadata": {}
    }
    response = requests.post(f"{BASE_URL}/rubrics", json=custom_rubric)
    print_response("Create Custom Rubric", response)


def example_weight_config_operations():
    """Example: Weight Configuration operations."""
    print("\n" + "="*60)
    print("WEIGHT CONFIGURATION EXAMPLES")
    print("="*60)
    
    # Get all weight configurations
    response = requests.get(f"{BASE_URL}/weight-configs")
    print_response("Get All Weight Configurations", response)
    
    # Create a weight configuration from existing rubrics
    response = requests.post(
        f"{BASE_URL}/weight-configs/from-rubrics",
        json={
            "name": "Comprehensive Code Evaluation",
            "rubric_ids": ["rubric_code_quality", "rubric_accuracy"],
            "weights": [0.6, 0.4],
            "domain_id": "domain_coding",
            "normalization_method": "weighted_average"
        }
    )
    print_response("Create Weight Config from Rubrics", response)
    
    if response.status_code == 201:
        config_id = response.json()["id"]
        
        # Get specific weight configuration
        response = requests.get(f"{BASE_URL}/weight-configs/{config_id}")
        print_response(f"Get Weight Config by ID ({config_id})", response)
        
        # Create a custom weight configuration
        custom_config = {
            "name": "Balanced Math Evaluation",
            "domain_id": "domain_math",
            "description": "Balanced configuration for mathematical evaluation",
            "rubric_weights": {
                "rubric_accuracy": {
                    "rubric_id": "rubric_accuracy",
                    "weight": 0.6,
                    "enabled": True
                },
                "rubric_reasoning": {
                    "rubric_id": "rubric_reasoning",
                    "weight": 0.4,
                    "enabled": True
                }
            },
            "normalization_method": "weighted_average",
            "metadata": {}
        }
        response = requests.post(f"{BASE_URL}/weight-configs", json=custom_config)
        print_response("Create Custom Weight Configuration", response)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("LLM EVALUATOR - LAYER 1 API EXAMPLES")
    print("="*60)
    print("\nMake sure the API server is running:")
    print("  uvicorn app.main:app --reload")
    print("\nPress Enter to continue...")
    input()
    
    try:
        # Test if server is running
        response = requests.get("http://localhost:8000/health")
        if response.status_code != 200:
            print("Error: Server is not running or not healthy")
            exit(1)
        
        # Run examples
        example_domain_operations()
        example_rubric_operations()
        example_weight_config_operations()
        
        print("\n" + "="*60)
        print("EXAMPLES COMPLETED")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
        print("Please make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"\nError: {e}")


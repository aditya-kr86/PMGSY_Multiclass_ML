"""
Test cases for quick form auto-fill during demonstrations.
Each test case represents a different PMGSY scheme type.
"""

TEST_CASES = [
    {
        "name": "1️⃣ PMGSY-I Project",
        "icon": "1️⃣",
        "scheme": "PMGSY-I",
        "data": {
            "state": "Andhra Pradesh",
            "district": "East Godavari",
            "road_sanctioned": 500,
            "length_sanctioned": 1400.00,
            "bridges_sanctioned": 20,
            "cost_sanctioned": 340.00,
            "road_completed": 498,
            "length_completed": 1308.00,
            "bridges_completed": 17,
            "expenditure": 320.00,
            "road_balance": 2,
            "length_balance": 92.00,
            "bridges_balance": 3
        }
    },
    {
        "name": "2️⃣ PMGSY-II Project",
        "icon": "2️⃣",
        "scheme": "PMGSY-II",
        "data": {
            "state": "Andhra Pradesh",
            "district": "Guntur",
            "road_sanctioned": 13,
            "length_sanctioned": 141.00,
            "bridges_sanctioned": 1,
            "cost_sanctioned": 78.00,
            "road_completed": 13,
            "length_completed": 141.00,
            "bridges_completed": 1,
            "expenditure": 69.70,
            "road_balance": 0,
            "length_balance": 0.00,
            "bridges_balance": 0
        }
    },
    {
        "name": "3️⃣ PMGSY-III Project",
        "icon": "3️⃣",
        "scheme": "PMGSY-III",
        "data": {
            "state": "Andhra Pradesh",
            "district": "Kurnool",
            "road_sanctioned": 23,
            "length_sanctioned": 216.00,
            "bridges_sanctioned": 3,
            "cost_sanctioned": 134.00,
            "road_completed": 19,
            "length_completed": 173.00,
            "bridges_completed": 1,
            "expenditure": 96.30,
            "road_balance": 4,
            "length_balance": 43.00,
            "bridges_balance": 2
        }
    },
    {
        "name": "🌉 RCPLWEA Project",
        "icon": "🌉",
        "scheme": "RCPLWEA",
        "data": {
            "state": "Bihar",
            "district": "Banka",
            "road_sanctioned": 11,
            "length_sanctioned": 183.00,
            "bridges_sanctioned": 16,
            "cost_sanctioned": 272.00,
            "road_completed": 11,
            "length_completed": 181.00,
            "bridges_completed": 16,
            "expenditure": 216.00,
            "road_balance": 0,
            "length_balance": 2.00,
            "bridges_balance": 0
        }
    },
    {
        "name": "👥 PM-JANMAN Project",
        "icon": "👥",
        "scheme": "PM-JANMAN",
        "data": {
            "state": "Andhra Pradesh",
            "district": "West Godavari",
            "road_sanctioned": 5,
            "length_sanctioned": 22.00,
            "bridges_sanctioned": 0,
            "cost_sanctioned": 15.00,
            "road_completed": 0,
            "length_completed": 0.00,
            "bridges_completed": 0,
            "expenditure": 0.00,
            "road_balance": 5,
            "length_balance": 22.00,
            "bridges_balance": 0
        }
    }
]


def get_test_case(index: int) -> dict:
    """
    Get a test case by index.
    
    Args:
        index: Test case index (0-2)
        
    Returns:
        Dictionary with test case data
    """
    if 0 <= index < len(TEST_CASES):
        return TEST_CASES[index]
    return TEST_CASES[0]


def get_all_test_cases() -> list:
    """Get all available test cases."""
    return TEST_CASES

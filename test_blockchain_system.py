#!/usr/bin/env python3
"""
Test script for the Land Registry Blockchain System
"""

import sys
import json
from templates.land_registry import LandRegistry

def test_blockchain_system():
    """Test the complete blockchain system functionality"""
    print("🔗 Testing Land Registry Blockchain System")
    print("=" * 50)
    
    # Initialize the land registry
    registry = LandRegistry()
    
    # Test 1: Register a new land
    print("\n📝 Test 1: Registering new land...")
    result1 = registry.register_land(
        land_id="LAND001",
        owner_name="John Doe",
        owner_address="123 Main Street, New York, NY 10001",
        land_details={
            "area": 2500,
            "location": "Downtown Manhattan",
            "land_type": "commercial",
            "survey_number": "SY-2024-001",
            "description": "Prime commercial property in downtown area"
        }
    )
    
    if result1['success']:
        print(f"✅ {result1['message']}")
        print(f"   Transaction Hash: {result1['transaction_hash'][:16]}...")
    else:
        print(f"❌ {result1['message']}")
        return False
    
    # Test 2: Register another land
    print("\n📝 Test 2: Registering second land...")
    result2 = registry.register_land(
        land_id="LAND002",
        owner_name="Jane Smith",
        owner_address="456 Oak Avenue, Los Angeles, CA 90210",
        land_details={
            "area": 1800,
            "location": "Beverly Hills",
            "land_type": "residential",
            "survey_number": "SY-2024-002",
            "description": "Luxury residential property"
        }
    )
    
    if result2['success']:
        print(f"✅ {result2['message']}")
    else:
        print(f"❌ {result2['message']}")
        return False
    
    # Test 3: Transfer land ownership
    print("\n🔄 Test 3: Transferring land ownership...")
    result3 = registry.transfer_land(
        land_id="LAND001",
        from_owner="123 Main Street, New York, NY 10001",
        to_owner="789 Business Blvd, Chicago, IL 60601",
        to_owner_name="ABC Corporation",
        transfer_details={
            "transfer_reason": "sale",
            "transfer_amount": "1500000",
            "notes": "Commercial property sale to corporation"
        }
    )
    
    if result3['success']:
        print(f"✅ {result3['message']}")
    else:
        print(f"❌ {result3['message']}")
        return False
    
    # Test 4: Get land information
    print("\n🔍 Test 4: Retrieving land information...")
    land_info = registry.get_land_info("LAND001")
    
    if land_info['success']:
        print(f"✅ Land ID: {land_info['land_id']}")
        print(f"   Current Owner: {land_info['current_owner']}")
        print(f"   Transaction Count: {land_info['transaction_count']}")
    else:
        print(f"❌ {land_info['message']}")
        return False
    
    # Test 5: Get all lands
    print("\n📋 Test 5: Getting all registered lands...")
    all_lands = registry.get_all_lands()
    print(f"✅ Total registered lands: {len(all_lands)}")
    
    for land in all_lands:
        print(f"   - {land['land_id']}: {land['current_owner'][:30]}...")
    
    # Test 6: Verify blockchain integrity
    print("\n🔐 Test 6: Verifying blockchain integrity...")
    is_valid = registry.verify_blockchain_integrity()
    
    if is_valid:
        print("✅ Blockchain integrity verified - all blocks are valid")
    else:
        print("❌ Blockchain integrity compromised")
        return False
    
    # Test 7: Get blockchain statistics
    print("\n📊 Test 7: Getting blockchain statistics...")
    stats = registry.get_blockchain_stats()
    
    print(f"✅ Blockchain Statistics:")
    print(f"   - Total Blocks: {stats['total_blocks']}")
    print(f"   - Total Transactions: {stats['total_transactions']}")
    print(f"   - Lands Registered: {stats['total_lands_registered']}")
    print(f"   - Land Transfers: {stats['total_transfers']}")
    print(f"   - Blockchain Valid: {stats['blockchain_valid']}")
    
    # Test 8: Try to register duplicate land (should fail)
    print("\n🚫 Test 8: Testing duplicate land registration (should fail)...")
    result8 = registry.register_land(
        land_id="LAND001",  # Duplicate ID
        owner_name="Test User",
        owner_address="Test Address",
        land_details={"area": 1000, "location": "Test Location", "land_type": "residential"}
    )
    
    if not result8['success']:
        print(f"✅ Correctly rejected duplicate: {result8['message']}")
    else:
        print(f"❌ Should have rejected duplicate registration")
        return False
    
    # Test 9: Try to transfer non-existent land (should fail)
    print("\n🚫 Test 9: Testing transfer of non-existent land (should fail)...")
    result9 = registry.transfer_land(
        land_id="LAND999",  # Non-existent
        from_owner="Test Owner",
        to_owner="New Owner",
        to_owner_name="New Owner Name",
        transfer_details={"transfer_reason": "sale"}
    )
    
    if not result9['success']:
        print(f"✅ Correctly rejected non-existent land: {result9['message']}")
    else:
        print(f"❌ Should have rejected non-existent land transfer")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Land Registry Blockchain System is working correctly!")
    print("\n🌐 You can now access the web interface at: http://127.0.0.1:5000")
    print("\n📋 Available features:")
    print("   • Register new land parcels")
    print("   • Transfer land ownership")
    print("   • View all land records")
    print("   • Explore blockchain transactions")
    print("   • Verify blockchain integrity")
    
    return True

if __name__ == "__main__":
    try:
        success = test_blockchain_system()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

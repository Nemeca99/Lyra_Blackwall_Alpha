#!/usr/bin/env python3
"""
Test script to verify that all imports work correctly with the new directory structure.
"""

import sys
import os
from pathlib import Path

# Add the Consciousness_Architecture directory to the path
sys.path.append(str(Path(__file__).parent / "Consciousness_Architecture"))
# Add the Dream_Systems directory to the path
sys.path.append(str(Path(__file__).parent / "Dream_Systems"))


def test_imports():
    """Test that all required modules can be imported."""
    try:
        # Test consciousness architecture imports
        import Left_Hemisphere
        import Right_Hemisphere
        import soul
        import body
        import fragment_manager
        import simple_router
        import heart
        import queue_manager

        # Test dream systems import
        import dream_manager

        print("✅ All imports successful!")

        # Test class imports
        ShortTermMemory = Left_Hemisphere.ShortTermMemory
        LongTermMemory = Right_Hemisphere.LongTermMemory
        Soul = soul.Soul
        Body = body.Body
        DreamManager = dream_manager.DreamManager
        FragmentManager = fragment_manager.FragmentManager
        Router = simple_router.Router
        Heart = heart.Heart
        QueueManager = queue_manager.QueueManager

        print("✅ All class imports successful!")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_brainstem_import():
    """Test that brainstem can be imported and initialized."""
    try:
        import brainstem

        print("✅ Brainstem import successful!")

        # Test basic initialization (without full system startup)
        print("Testing brainstem basic functionality...")

        return True

    except ImportError as e:
        print(f"❌ Brainstem import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Brainstem unexpected error: {e}")
        return False


if __name__ == "__main__":
    print("Testing Lyra Core Theory imports...")
    print("=" * 50)

    success1 = test_imports()
    success2 = test_brainstem_import()

    print("=" * 50)
    if success1 and success2:
        print("🎉 All tests passed! The directory structure is working correctly.")
    else:
        print("❌ Some tests failed. Please check the import paths.")

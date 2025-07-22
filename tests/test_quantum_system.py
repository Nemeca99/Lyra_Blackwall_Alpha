"""
Test Quantum Superposition System with Your Configuration
Tests the quantum kitchen with your specific LM Studio setup
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from quantum_kitchen import QuantumChef, QuantumOrder


async def test_quantum_system():
    """Test the quantum superposition system with your configuration"""
    print("🌊 Testing Quantum Superposition System...")
    print("🔬 Using your LM Studio configuration:")
    print("   • URL: http://169.254.83.107:1234")
    print("   • Model: deepseek/deepseek-r1-0528-qwen3-8b")
    print("   • Channel ID: 1380754964317601813")

    # Initialize quantum chef with your configuration
    quantum_chef = QuantumChef(
        lm_studio_url="http://169.254.83.107:1234/v1/chat/completions",
        ollama_url="http://localhost:11434",
    )

    print("\n👨‍🍳 Quantum Chef initialized!")

    # Test quantum order
    order = QuantumOrder(
        user_id="test_user_quantum",
        message="Hello! I'm testing the quantum superposition AI system with your DeepSeek model!",
        format_type="text",
    )

    print(f"\n📝 Testing quantum order: {order.superposition_id}")

    try:
        # Test quantum collapse
        print("🔬 Starting quantum superposition collapse...")
        collapsed_response = await quantum_chef.observe_and_collapse(order)

        print(f"\n✅ Quantum collapse completed!")
        print(f"👤 User: {collapsed_response.user_id}")
        print(f"📝 Response: {collapsed_response.response_content[:200]}...")
        print(f"🎯 Personalization: {collapsed_response.personalization_level:.1%}")
        print(
            f"⚛️ Particle Confidence: {collapsed_response.particle_contribution.confidence}"
        )
        print(
            f"🌊 Wave Emotions: {collapsed_response.wave_contribution.emotion_profile}"
        )
        print(f"💥 Collapse Time: {collapsed_response.collapse_time:.2f}s")
        print(
            f"⚡ Total Processing: {collapsed_response.particle_contribution.processing_time + collapsed_response.wave_contribution.processing_time:.2f}s"
        )

        # Get quantum status
        status = quantum_chef.get_quantum_status()
        print(f"\n📊 Quantum Status:")
        print(f"   • Total Collapses: {status['total_collapses']}")
        print(
            f"   • Success Rate: {status['successful_collapses']}/{status['total_collapses']}"
        )
        print(f"   • Average Collapse Time: {status['average_collapse_time']:.2f}s")
        print(f"   • Quantum Efficiency: {status['quantum_efficiency']:.1%}")

        print("\n🎉 Quantum Superposition System test completed successfully!")
        print("🚀 Ready to start the quantum Discord bot!")

    except Exception as e:
        print(f"\n❌ Error in quantum test: {e}")
        print("🔧 Please check:")
        print("   • LM Studio is running on http://169.254.83.107:1234")
        print("   • DeepSeek model is loaded")
        print("   • Ollama is running on localhost:11434")


if __name__ == "__main__":
    asyncio.run(test_quantum_system())

import sys
from engine.dependencies import get_simulation_instance
from engine.replay_engine import Engine

def test_engine_boot():
    print("--- Running Engine Boot Test ---")
    
    simulation_instance = get_simulation_instance()
    engine = Engine(simulation_instance)

    assert engine is not None, "Engine instance should not be None."
    assert engine._simulation is not None, "Engine's internal simulation instance should not be None."
    
    print("Engine Boot Test: PASSED - Engine initialized successfully with simulation instance.")

if __name__ == "__main__":
    try:
        test_engine_boot()
    except AssertionError as e:
        print(f"Engine Boot Test: FAILED - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during Engine Boot Test: {e}")
        sys.exit(1)
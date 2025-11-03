import random
import time
from datetime import datetime
import newrelic.agent # Import the New Relic Agent
newrelic.agent.initialize('newrelic.ini')

# --- New Relic Initialization ---
# The agent will look for a 'newrelic.ini' file in your current
# directory or specified path. Replace '/path/to/newrelic.ini' 
# with the actual path to your configuration file if it's not local.
try:
    # Initialize the agent. This must happen before any monitored code runs.
    # Set 'environment' to 'staging', 'production', etc., as needed.
    newrelic.agent.initialize('newrelic.ini', environment='development')
    print("New Relic Agent successfully initialized.")
except Exception as e:
    print(f"Warning: New Relic initialization failed. Data will not be reported. Error: {e}")

# --- Configuration ---
ROLL_INTERVAL_SECONDS = 5
DICE_SIDES = 6

# The agent automatically ignores simple helper functions like this.
def roll_dice():
    """
    Simulates the roll of a standard six-sided die.
    """
    return random.randint(1, DICE_SIDES)

# --- Instrumented Task ---
@newrelic.agent.background_task(name='DiceRoll', group='AutomaticRolls')
def perform_single_roll(roll_count: int) -> None:
    """
    Performs one dice roll, records it as a New Relic background transaction,
    and adds custom attributes for analysis.
    """
    # 1. Get the current time for logging
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. Roll the dice (the core work of the transaction)
    result = roll_dice()

    # 3. Add Custom Attributes 

    
    # 4. Print the output
    print(f"[{timestamp}] Roll #{roll_count}: The dice landed on: {result}")


def start_automatic_rolls():
    """
    Starts an infinite loop to execute the instrumented roll_dice function 
    at the specified interval.
    """
    print("\n--- Automatic Dice Roller Started ---")
    print(f"Rolling a D{DICE_SIDES} every {ROLL_INTERVAL_SECONDS} seconds.")
    print("Press Ctrl+C to stop the application.\n")

    roll_count = 0
    while True:
        try:
            roll_count += 1
            
            # --- Key Change ---
            # Call the instrumented function. New Relic sees this as 
            # the start and end of a 'DiceRoll' background task transaction.
            perform_single_roll(roll_count)
            # --- End Key Change ---

            # Wait for the specified interval
            time.sleep(ROLL_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            # Handle user interruption (Ctrl+C) gracefully
            print("\n--- Dice Roller Stopped ---")
            break
        except Exception as e:
            # Handle any unexpected errors
            print(f"\nAn error occurred: {e}")
            time.sleep(ROLL_INTERVAL_SECONDS) # Wait before trying again

if __name__ == "__main__":
    start_automatic_rolls()

#!/usr/bin/env python3

import os
import sys
import traceback
import json

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


def check_dependencies():
    """Check if required modules can be imported"""
    missing_modules = []

    try:
        from phishing_model_trainer import PhishingAwarenessModelTrainer
        print("✅ phishing_model_trainer module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import phishing_model_trainer: {e}")
        missing_modules.append("phishing_model_trainer")

    try:
        from phishing_user_tester import PhishingAwarenessTester
        print("✅ phishing_user_tester module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import phishing_user_tester: {e}")
        missing_modules.append("phishing_user_tester")

    try:
        from phishing_educational_resources import PhishingEducationalResourceManager
        print("✅ phishing_educational_resources module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import phishing_educational_resources: {e}")
        missing_modules.append("phishing_educational_resources")

    return missing_modules


def check_json_structure():
    """Check the structure of the phishing JSON answer sheet"""
    if not os.path.exists('answer_sheetphi.json'):
        print("❌ answer_sheetphi.json not found")
        return False

    try:
        with open('answer_sheetphi.json', 'r') as f:
            data = json.load(f)

        print(f"\nPhishing JSON Structure Analysis:")
        print(f"Type: {type(data)}")
        print(
            f"Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dictionary'}")

        if isinstance(data, dict):
            for key, value in data.items():
                print(f"  '{key}': {type(value)}")
                if isinstance(value, dict):
                    print(f"    Subkeys: {list(value.keys())[:5]}...")
                elif isinstance(value, list):
                    print(f"    Length: {len(value)}")
                    if len(value) > 0:
                        print(f"    First item: {type(value[0])}")

        return True
    except Exception as e:
        print(f"❌ Error reading phishing JSON: {e}")
        return False


def check_files():
    """Check if required phishing files exist"""
    files_to_check = [
        'phishing_form.csv',
        'answer_sheetphi.json'
    ]

    print(f"\nCurrent working directory: {os.getcwd()}")
    print(f"Script directory: {current_dir}")
    print("\nChecking required phishing files:")

    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} (size: {size} bytes)")
        else:
            print(f"❌ {file} not found")


def main():
    print("Phishing Awareness Assessment System")
    print("=" * 50)

    # Check dependencies first
    print("\nChecking dependencies...")
    missing_modules = check_dependencies()

    if missing_modules:
        print(f"\n❌ Missing required modules: {', '.join(missing_modules)}")
        print("Please ensure all required Python files are in the same directory.")
        return

    # Import modules after checking
    try:
        from phishing_model_trainer import PhishingAwarenessModelTrainer
        from phishing_user_tester import PhishingAwarenessTester
        from phishing_educational_resources import PhishingEducationalResourceManager
    except ImportError as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return

    # Initialize educational manager
    education_manager = PhishingEducationalResourceManager()
    last_quiz_score = None
    weak_areas = []

    while True:
        print("\nSelect an option:")
        print("1. Train ML Model")
        print("2. Take Assessment Quiz")
        print("3. Educational Resources & Learning")
        print("4. Check System Status")
        print("5. Check JSON Structure")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            print("\n--- Training Phishing Awareness ML Model ---")
            check_files()

            # Check JSON structure first
            if not check_json_structure():
                print("❌ Phishing JSON structure check failed!")
                continue

            # Check if required files exist
            if not os.path.exists('phishing_form.csv'):
                print("Error: phishing_form.csv not found!")
                print(
                    "Please ensure the phishing dataset file is in the current directory.")
                continue

            if not os.path.exists('answer_sheetphi.json'):
                print("Error: answer_sheetphi.json not found!")
                print(
                    "Please ensure the phishing answer sheet file is in the current directory.")
                continue

            try:
                print("Initializing phishing awareness trainer...")
                trainer = PhishingAwarenessModelTrainer(
                    dataset_path='phishing_form.csv',
                    answer_sheet_path='answer_sheetphi.json'
                )

                print("Starting phishing awareness model training...")
                model, accuracy = trainer.train_model()
                print(f"\n✅ Phishing model training completed successfully!")
                print(f"Model accuracy: {accuracy:.2f}")

            except Exception as e:
                print(f"❌ Error during phishing model training: {e}")
                traceback.print_exc()

        elif choice == '2':
            print("\n--- Phishing Awareness Assessment ---")

            # Check if model exists
            if not os.path.exists('phishing_awareness_model.pkl'):
                print("❌ Trained phishing model not found!")
                print("Please train the model first (option 1).")
                continue

            try:
                print("Initializing phishing awareness tester...")
                tester = PhishingAwarenessTester()
                result = tester.run_assessment()

                # Store results for educational recommendations
                if isinstance(result, dict):
                    last_quiz_score = result.get('score', 0)
                    weak_areas = result.get('weak_areas', [])

                    print(
                        f"\n🎯 Ready to strengthen your phishing defenses? Check out option 3!")
                elif isinstance(result, (int, float)):
                    last_quiz_score = result
                    print(
                        f"\n🎯 Ready to learn more about phishing prevention? Check out option 3!")

            except Exception as e:
                print(f"❌ Error during phishing assessment: {e}")
                traceback.print_exc()

        elif choice == '3':
            print("\n--- Phishing Defense Educational Resources & Learning ---")
            try:
                if last_quiz_score is not None:
                    print(f"📊 Using your recent phishing assessment results...")
                    education_manager.run_educational_session(
                        last_quiz_score, weak_areas)
                else:
                    print(
                        "📚 No recent assessment found. Showing general phishing resources...")
                    education_manager.run_educational_session()

                # Offer additional options
                print(f"\n🔄 Additional Phishing Defense Options:")
                print("A. View resources for different knowledge level")
                print("B. Get quick phishing prevention tips")
                print("C. Return to main menu")

                sub_choice = input(
                    "\nEnter your choice (A/B/C): ").strip().upper()

                if sub_choice == 'A':
                    education_manager.run_educational_session()
                elif sub_choice == 'B':
                    tips = education_manager.get_interactive_tips()
                    print(f"\n🎯 PHISHING PREVENTION TIPS:")
                    for i, tip in enumerate(tips, 1):
                        print(f"{i}. {tip}")

            except Exception as e:
                print(f"❌ Error accessing phishing educational resources: {e}")
                traceback.print_exc()

        elif choice == '4':
            print("\n--- Phishing System Status ---")
            check_files()

            # Check for model file
            if os.path.exists('phishing_awareness_model.pkl'):
                size = os.path.getsize('phishing_awareness_model.pkl')
                print(f"✅ phishing_awareness_model.pkl (size: {size} bytes)")
            else:
                print("❌ phishing_awareness_model.pkl not found")

            if os.path.exists('phishing_feature_names.pkl'):
                size = os.path.getsize('phishing_feature_names.pkl')
                print(f"✅ phishing_feature_names.pkl (size: {size} bytes)")
            else:
                print("❌ phishing_feature_names.pkl not found")

        elif choice == '5':
            print("\n--- Phishing JSON Structure Check ---")
            check_json_structure()

        elif choice == '6':
            print("\nThank you for using the Phishing Awareness Assessment System!")
            print("Stay vigilant and keep your defenses strong! 🛡️🎯")
            break

        else:
            print("Invalid choice! Please enter 1, 2, 3, 4, 5, or 6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        traceback.print_exc()

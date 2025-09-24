# phishing_user_tester_fixed.py
import json
import joblib
import pandas as pd
import numpy as np
import os

# Import your enhancer - ensure phishing_knowledge_enhancer.py is in the same folder or in PYTHONPATH
try:
    from phishing_knowledge_enhancer import PhishingKnowledgeEnhancer
except Exception:
    # Provide a minimal fallback so the tester still runs if the enhancer isn't available.
    class PhishingKnowledgeEnhancer:
        def get_enhancement_advice(self, question, level):
            return "Review official guidance on phishing recognition (check sender, links, urgency)."

        def get_detailed_guidance(self, question, level):
            return "Practice identifying suspicious senders and never enter credentials via email links."


class PhishingAwarenessTester:
    def __init__(self,
                 answer_sheet_path='answer_sheetphi.json',
                 model_path='phishing_awareness_model.pkl',
                 feature_names_path='phishing_feature_names.pkl'):
        self.answer_sheet_path = answer_sheet_path
        self.model_path = model_path
        self.feature_names_path = feature_names_path

        self.answer_sheet = None
        self.questions_data = None
        self.model = None
        self.feature_names = None
        self.enhancer = PhishingKnowledgeEnhancer()

        self.load_components()

    def load_components(self):
        """Load trained model and answer sheet"""
        try:
            if not os.path.exists(self.answer_sheet_path):
                raise FileNotFoundError(self.answer_sheet_path)

            with open(self.answer_sheet_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.answer_sheet = {}
            self.questions_data = []

            if 'questions' in data and isinstance(data['questions'], list):
                for q_item in data['questions']:
                    question_text = q_item.get('question')
                    if not question_text:
                        continue

                    options_dict = {}
                    for option in q_item.get('options', []):
                        opt_text = option.get('text', '')
                        options_dict[opt_text] = {
                            'weight': option.get('marks', 0),
                            'level': option.get('level', None)
                        }

                    self.answer_sheet[question_text] = options_dict
                    self.questions_data.append(q_item)

            # Load model and feature names if they exist (optional for quiz)
            if os.path.exists(self.model_path):
                try:
                    self.model = joblib.load(self.model_path)
                except Exception as e:
                    print(
                        f"[WARN] Could not load model '{self.model_path}': {e}")
                    self.model = None

            if os.path.exists(self.feature_names_path):
                try:
                    self.feature_names = joblib.load(self.feature_names_path)
                except Exception as e:
                    print(
                        f"[WARN] Could not load feature names '{self.feature_names_path}': {e}")
                    self.feature_names = None

            print("[INFO] Phishing components loaded successfully!")
            print(
                f"[INFO] Loaded {len(self.questions_data)} phishing awareness questions for quiz")

        except FileNotFoundError as e:
            print(f"[ERROR] Answer sheet not found: {e}")
            print(
                "Please run phishing_model_trainer.py first to create the answer sheet.")
            self.answer_sheet = {}
            self.questions_data = []

    def conduct_quiz(self):
        """Conduct interactive phishing awareness quiz with user"""
        if not self.questions_data:
            print("[ERROR] No questions available to conduct quiz.")
            return {}, {}

        print("\n=== PHISHING AWARENESS ASSESSMENT QUIZ ===")
        print("Test your knowledge about identifying and preventing phishing attacks.\n")

        user_responses = {}
        user_scores = {}

        for i, q_item in enumerate(self.questions_data, 1):
            question = q_item.get('question', 'No question text provided')
            options = q_item.get('options', [])

            print(f"Question {i}: {question}\n")
            for j, option in enumerate(options, 1):
                print(f"{j}. {option.get('text', '')}")

            # If running in a non-interactive environment, default to the best (highest marks) option
            try:
                if os.getenv('NON_INTERACTIVE', '0') == '1':
                    # choose highest-mark option automatically
                    best_opt = max(options, key=lambda o: o.get('marks', 0))
                    selected_option = best_opt
                    print(
                        f"\n[NON-INTERACTIVE] Selecting: {best_opt.get('text')}")
                else:
                    while True:
                        try:
                            choice = int(
                                input(f"\nEnter your choice (1-{len(options)}): "))
                            if 1 <= choice <= len(options):
                                selected_option = options[choice - 1]
                                break
                            else:
                                print("Please enter a valid choice!")
                        except ValueError:
                            print("Please enter a valid number!")
            except KeyboardInterrupt:
                print("\n[INFO] Quiz interrupted by user.")
                break

            selected_answer = selected_option.get('text', '')
            user_responses[question] = selected_answer
            user_scores[question] = {
                'answer': selected_answer,
                'score': selected_option.get('marks', 0),
                'level': selected_option.get('level', 'Unknown')
            }

            print("-" * 50)

        return user_responses, user_scores

    def calculate_results(self, user_scores):
        """Calculate overall phishing awareness results"""
        if not user_scores:
            return 0, 0.0, 'Beginner'

        total_score = sum(float(score_info.get('score', 0))
                          for score_info in user_scores.values())
        max_possible_score = len(user_scores) * \
            10.0 if len(user_scores) > 0 else 1.0
        percentage = (total_score / max_possible_score) * \
            100.0 if max_possible_score > 0 else 0.0

        if percentage >= 75:
            overall_level = 'Expert'
        elif percentage >= 50:
            overall_level = 'Intermediate'
        elif percentage >= 25:
            overall_level = 'Basic'
        else:
            overall_level = 'Beginner'

        return total_score, percentage, overall_level

    def provide_feedback(self, user_scores, overall_level, percentage):
        """Provide detailed feedback and phishing prevention recommendations"""
        print("\n" + "="*60)
        print("PHISHING AWARENESS QUIZ RESULTS & PERSONALIZED FEEDBACK")
        print("="*60)

        total_score = sum(float(score_info.get('score', 0))
                          for score_info in user_scores.values())
        print(
            f"Total Score: {int(total_score)}/{len(user_scores) * 10 if user_scores else 100}")
        print(f"Percentage: {percentage:.1f}%")
        print(f"Overall Phishing Awareness Level: {overall_level}")

        if percentage >= 75:
            print("\n🎉 Excellent! You're well-protected against phishing attacks!")
        else:
            print("\n⚠️ Important: You need to improve your phishing awareness.")

        print("\n" + "-"*60)
        print("DETAILED ANALYSIS BY QUESTION:")
        print("-"*60)

        improvement_areas = []

        for i, (question, score_info) in enumerate(user_scores.items(), 1):
            level = score_info.get('level', 'Unknown')
            score = float(score_info.get('score', 0))

            print(f"\nQuestion {i}: {question}")
            print(
                f"Your Answer Level: {str(level).upper()} ({int(score)}/10 points)")

            if score < 10:
                improvement_areas.append({
                    'question': question,
                    'current_level': level,
                    'score': score
                })

                print(f"🎯 Phishing Defense Enhancement:")
                recommendation = self.enhancer.get_enhancement_advice(
                    question, level)
                print(f"   {recommendation}")

        if improvement_areas:
            print("\n" + "="*60)
            print("PRIORITY PHISHING PROTECTION AREAS:")
            print("="*60)

            # show up to top-3 worst scoring areas
            improvement_areas.sort(key=lambda x: x['score'])
            for area in improvement_areas[:3]:
                print(f"\n🚨 Critical Area: {area['question']}")
                print(f"   Current Level: {area['current_level']}")
                enhanced_advice = self.enhancer.get_detailed_guidance(
                    area['question'], area['current_level'])
                print(f"   🛡️ Protection Strategy: {enhanced_advice}")

    def run_assessment(self):
        """Run complete phishing awareness assessment process"""
        if not self.answer_sheet or not self.questions_data:
            print(
                "Error: Answer sheet or questions not loaded. Please prepare the answer sheet.")
            return None

        # Conduct quiz
        user_responses, user_scores = self.conduct_quiz()

        # Calculate results
        total_score, percentage, overall_level = self.calculate_results(
            user_scores)

        # Provide feedback
        self.provide_feedback(user_scores, overall_level, percentage)

        # Save user results
        user_data = {
            'responses': user_responses,
            'scores': user_scores,
            'total_score': total_score,
            'percentage': percentage,
            'overall_level': overall_level,
            'assessment_type': 'phishing_awareness'
        }

        try:
            with open('user_phishing_assessment_results.json', 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Results saved to 'user_phishing_assessment_results.json'")
        except Exception as e:
            print(f"[WARN] Could not save results: {e}")

        # Return useful summary for programmatic use
        weak_areas = [q for q, s in user_scores.items() if float(
            s.get('score', 0)) < 7]
        return {
            'score': percentage,
            'weak_areas': weak_areas
        }


if __name__ == "__main__":
    tester = PhishingAwarenessTester()
    summary = tester.run_assessment()
    if summary is not None:
        print("\nSummary:", summary)

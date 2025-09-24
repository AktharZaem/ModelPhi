import json
import joblib
import pandas as pd
import numpy as np
import os
import requests
from phishing_knowledge_enhancer import PhishingKnowledgeEnhancer


class PhishingTester:
    def __init__(self):
        self.answer_sheet = None
        self.questions_data = None
        self.model = None
        self.feature_names = None
        self.enhancer = PhishingKnowledgeEnhancer()
        self.gemini_api_key = os.getenv(
            'GEMINI_API_KEY') or "AIzaSyDuDJ5uyh3DBAjEFTHaCz-g25fH7hp72Yc"
        self.load_components()

    def load_components(self):
        """Load trained model and answer sheet"""
        try:
            # Load answer sheet and parse the nested structure
            with open('answer_sheetphi.json', 'r') as f:
                data = json.load(f)

            self.answer_sheet = {}
            self.questions_data = []

            if 'questions' in data and isinstance(data['questions'], list):
                for q_item in data['questions']:
                    question_text = q_item['question']
                    options_dict = {}

                    for option in q_item['options']:
                        options_dict[option['text']] = {
                            'weight': option['marks'],
                            'level': option['level']
                        }

                    self.answer_sheet[question_text] = options_dict
                    self.questions_data.append(q_item)

            # Load trained model
            self.model = joblib.load('phishing_model.pkl')
            self.feature_names = joblib.load('phishing_feature_names.pkl')

            print("Phishing components loaded successfully!")
            print(f"Loaded {len(self.questions_data)} questions for quiz")

        except FileNotFoundError as e:
            print(f"Error loading components: {e}")
            print("Please run phishing_model_trainer.py first to train the model")

    def conduct_quiz(self):
        """Conduct interactive quiz with user"""
        print("\n=== Phishing Awareness Security Quiz ===")
        print("Please answer the following 10 questions about phishing awareness.\n")

        user_responses = {}
        user_scores = {}

        for i, q_item in enumerate(self.questions_data, 1):
            question = q_item['question']
            options = q_item['options']

            print(f"Question {i}: {question}")
            print("\nOptions:")

            # Display options
            for j, option in enumerate(options, 1):
                print(f"{j}. {option['text']}")

            # Get user input
            while True:
                try:
                    choice = int(
                        input(f"\nEnter your choice (1-{len(options)}): "))
                    if 1 <= choice <= len(options):
                        selected_option = options[choice - 1]
                        selected_answer = selected_option['text']

                        user_responses[question] = selected_answer

                        # Get score and level for this answer
                        user_scores[question] = {
                            'answer': selected_answer,
                            'score': selected_option['marks'],
                            'level': selected_option['level']
                        }
                        break
                    else:
                        print("Please enter a valid choice!")
                except ValueError:
                    print("Please enter a valid number!")

            print("-" * 50)

        return user_responses, user_scores

    def calculate_results(self, user_scores):
        """Calculate overall results and recommendations"""
        total_score = sum(score_info['score']
                          for score_info in user_scores.values())
        max_possible_score = len(user_scores) * 10
        percentage = (total_score / max_possible_score) * 100

        # Determine overall level
        if percentage >= 75:
            overall_level = 'Expert'
        elif percentage >= 50:
            overall_level = 'Intermediate'
        elif percentage >= 25:
            overall_level = 'Basic'
        else:
            overall_level = 'Beginner'

        return total_score, percentage, overall_level

    def get_gemini_explanation(self, question, current_level, overall_level):
        """Get personalized explanation from Gemini API"""
        if not self.gemini_api_key:
            return self.get_detailed_explanation(question, current_level, overall_level)

        try:
            # Clean question text for API call
            clean_question = question.replace('"', "'").replace('\n', ' ')
            
            prompt = f"""
You are an expert cybersecurity educator specializing in phishing awareness and email security.

CONTEXT:
- User's Question: "{clean_question}"
- User's Current Answer Level: {current_level}
- User's Overall Knowledge Level: {overall_level}

TASK:
Provide a personalized explanation to help this user understand this phishing concept and advance to the next level.

GUIDELINES:
- If user is at "wrong" level, explain the basics very simply (like explaining to a child)
- If user is at "beginner" level, provide more detailed explanations with examples
- If user is at "intermediate" level, give advanced concepts and best practices
- If user is at "advanced" level, provide expert-level insights and enterprise considerations

FORMAT:
- Use emojis and clear structure
- Include practical examples
- Explain WHY this matters for their security and privacy
- Give actionable next steps
- Keep it engaging and educational
- Maximum 300 words

Please provide a comprehensive explanation that will help them improve from their current level to the next level.
"""

            model_names = [
                "gemini-1.5-flash",
                "gemini-1.5-pro", 
                "gemini-1.0-pro",
                "gemini-pro"
            ]

            for model_name in model_names:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.gemini_api_key}"

                    headers = {
                        "Content-Type": "application/json"
                    }

                    data = {
                        "contents": [{
                            "parts": [{
                                "text": prompt
                            }]
                        }],
                        "generationConfig": {
                            "temperature": 0.7,
                            "topK": 40,
                            "topP": 0.95,
                            "maxOutputTokens": 500,
                        }
                    }

                    print(f"📚 AI analyzing for better learning experience...")
                    response = requests.post(url, headers=headers, json=data, timeout=30)

                    if response.status_code == 200:
                        result = response.json()
                        if 'candidates' in result and len(result['candidates']) > 0:
                            generated_text = result['candidates'][0]['content']['parts'][0]['text']
                            return f"\nPERSONALIZED EXPLANATION:\n{generated_text}"
                    else:
                        continue

                except Exception as model_error:
                    continue

            print("⚠️ Using fallback explanation")
            return self.get_detailed_explanation(question, current_level, overall_level)

        except Exception as e:
            print(f"⚠️ Error calling API: {e}")
            return self.get_detailed_explanation(question, current_level, overall_level)

    def get_detailed_explanation(self, question, current_level, overall_level):
        """Get detailed explanation based on question and user's overall knowledge level"""
        
        # Clean question for matching
        clean_question = question.lower().replace('"', '').replace('\n', ' ')
        
        explanations = {
            "email": {
                "wrong": """
🎣 WHAT IS PHISHING?
Think of phishing like a fisherman trying to catch fish with fake bait. Scammers send fake emails pretending to be from banks, companies, or people you know to "catch" your personal information.

🚨 WHAT TO DO:
• NEVER reply with personal details like passwords, credit card numbers, or social security numbers
• Don't click suspicious links or attachments
• If it seems urgent or scary, it's probably fake
• When in doubt, contact the company directly using their official website or phone number

💡 SIMPLE RULE: Real companies will NEVER ask for passwords or personal details via email!
""",
                "beginner": """
🔒 UNDERSTANDING PHISHING ATTACKS:
Phishing emails are designed to steal your personal information by impersonating legitimate organizations or creating a sense of urgency.

🛡️ BEST PRACTICES:
• Always verify the sender's email address carefully
• Look for spelling and grammar mistakes in the email
• Check if the email uses generic greetings like "Dear Customer"
• Hover over links without clicking to see the real destination
• Use two-factor authentication on important accounts

⚖️ VERIFICATION: When suspicious, independently verify by contacting the organization through official channels
""",
                "intermediate": """
🎯 ADVANCED PHISHING DEFENSE:
Implementing comprehensive anti-phishing strategies requires understanding attack vectors and implementing layered security controls.

🔬 ENTERPRISE CONSIDERATIONS:
• Deploy email security gateways with advanced threat protection
• Implement DMARC, SPF, and DKIM email authentication protocols
• Conduct regular phishing simulation training
• Monitor and analyze email headers for authentication failures
• Establish incident response procedures for phishing attacks

🏢 ORGANIZATIONAL SECURITY: Apply security awareness training and implement phishing-resistant authentication methods
"""
            }
        }

        # Determine category based on question content
        if any(keyword in clean_question for keyword in ['email', 'confirm', 'details', 'password', 'login', 'pop-up', 'link']):
            category = 'email'
        else:
            category = 'email'  # Default to email category

        if category in explanations and current_level.lower() in explanations[category]:
            return explanations[category][current_level.lower()]
        else:
            return f"""
📚 LEARNING OPPORTUNITY:
This question tests your understanding of phishing awareness. The key is to think about whether the request seems legitimate and what a scammer might be trying to accomplish.

🎯 NEXT STEPS:
• Research phishing tactics and red flags online
• Practice identifying suspicious emails
• Learn about email security best practices
• Consider taking a cybersecurity awareness course

💡 REMEMBER: When in doubt, verify through official channels before taking action!
"""

    def provide_feedback(self, user_scores, overall_level, percentage):
        """Provide detailed feedback and recommendations"""
        print("\n" + "="*60)
        print("PHISHING AWARENESS QUIZ RESULTS & PERSONALIZED FEEDBACK")
        print("="*60)

        total_score = sum(score_info['score']
                          for score_info in user_scores.values())
        print(f"Total Score: {total_score}/100")
        print(f"Percentage: {percentage:.1f}%")
        print(f"Overall Phishing Security Level: {overall_level}")

        # Provide level-specific encouragement
        if percentage >= 75:
            print("\n🎉 Congratulations! You're PHISHING-RESISTANT!")
            print("Your phishing awareness is excellent.")
            print("You can identify and avoid most phishing attempts effectively.")
        elif percentage >= 50:
            print("\n📈 Good Progress! You're at INTERMEDIATE level!")
            print("You have solid phishing awareness but there's room for improvement.")
            print("Focus on the areas below to reach expert level protection.")
        elif percentage >= 25:
            print("\n📚 You're at BASIC level - Learning Time!")
            print("Don't worry! Phishing can be tricky to detect.")
            print(
                "Think of phishing like strangers trying to trick you - be suspicious of unexpected requests!")
        else:
            print("\n🌱 You're just getting started - BEGINNER level!")
            print(
                "No problem at all! Let's learn how to spot phishing attempts together.")
            print("Remember: When in doubt, don't click or share personal information!")

        print("\n" + "-"*60)
        print("DETAILED ANALYSIS BY QUESTION:")
        print("-"*60)

        improvement_areas = []

        for i, (question, score_info) in enumerate(user_scores.items(), 1):
            level = score_info['level']
            score = score_info['score']

            print(f"\nQuestion {i}: {question}")
            print(f"Your Answer Level: {level.upper()} ({score}/10 points)")

            if score < 10:
                improvement_areas.append({
                    'question': question,
                    'current_level': level,
                    'score': score
                })

                ai_explanation = self.get_gemini_explanation(
                    question, level, overall_level)
                print(ai_explanation)

        # Overall recommendations
        if improvement_areas:
            print("\n" + "="*60)
            print("PRIORITY IMPROVEMENT AREAS:")
            print("="*60)

            improvement_areas.sort(key=lambda x: x['score'])

            for area in improvement_areas[:3]:
                print(f"\n🎯 Priority Question: {area['question']}")
                print(
                    f"   Your Current Level: {area['current_level'].upper()}")

                enhanced_advice = self.enhancer.get_detailed_guidance(
                    area['question'], area['current_level']
                )
                print(f"   📚 Learning Path: {enhanced_advice}")

        print("\n" + "="*60)
        if overall_level.lower() == 'beginner':
            print("🌟 REMEMBER: Every cybersecurity expert started as a beginner!")
            print("Take your time to learn - your digital safety is worth it!")
        elif overall_level.lower() == 'basic':
            print("🚀 YOU'RE MAKING PROGRESS!")
            print("Keep learning about phishing - you're building strong defenses!")
        elif overall_level.lower() == 'intermediate':
            print("🎯 ALMOST THERE!")
            print("Focus on the priority areas above to reach expert level!")
        else:
            print("🏆 EXCELLENT WORK!")
            print("You're well-equipped to identify and avoid phishing attacks!")

    def run_assessment(self):
        """Run complete assessment process"""
        if not self.model or not self.answer_sheet:
            print(
                "Error: Model or answer sheet not loaded. Please train the model first.")
            return

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
            'overall_level': overall_level
        }

        with open('phishing_assessment_results.json', 'w') as f:
            json.dump(user_data, f, indent=2)

        print(f"\n📄 Results saved to 'phishing_assessment_results.json'")

        return {
            'score': percentage,
            'weak_areas': [question for question, score_info in user_scores.items() if score_info['score'] < 7]
        }


if __name__ == "__main__":
    tester = PhishingTester()
    tester.run_assessment()

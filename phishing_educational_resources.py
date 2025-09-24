import json
from typing import List, Dict, Optional
import os


class PhishingEducationalResourceManager:
    def __init__(self):
        self.learning_resources = {
            'beginner': {
                'articles': [
                    {
                        'title': 'What is Phishing? - CISA Guide',
                        'url': 'https://www.cisa.gov/secure-our-world/avoid-phishing',
                        'description': 'Official CISA guide to understanding and avoiding phishing attacks'
                    },
                    {
                        'title': 'Phishing Awareness Basics - FTC',
                        'url': 'https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams',
                        'description': 'Federal Trade Commission guide on recognizing phishing scams'
                    }
                ]
            },
            'intermediate': {
                'articles': [
                    {
                        'title': 'Advanced Phishing Techniques',
                        'url': 'https://www.sans.org/reading-room/whitepapers/email/advanced-email-attacks-39020',
                        'description': 'SANS whitepaper on sophisticated email attack methods'
                    },
                    {
                        'title': 'Business Email Compromise Prevention',
                        'url': 'https://www.fbi.gov/how-we-can-help-you/safety-resources/scams-and-safety/common-scams-and-crimes/business-email-compromise',
                        'description': 'FBI resources on preventing business email compromise'
                    }
                ]
            },
            'advanced': {
                'articles': [
                    {
                        'title': 'Threat Intelligence for Phishing',
                        'url': 'https://www.mitre.org/publications/technical-papers/email-security',
                        'description': 'MITRE research on email security and threat intelligence'
                    }
                ]
            }
        }

    def assess_knowledge_level(self, quiz_score: float) -> str:
        """Determine phishing awareness level based on quiz performance"""
        if quiz_score >= 80:
            return 'advanced'
        elif quiz_score >= 60:
            return 'intermediate'
        else:
            return 'beginner'

    def get_learning_resources(self, knowledge_level: str) -> Dict:
        """Get curated phishing awareness resources based on knowledge level"""
        return self.learning_resources.get(knowledge_level, self.learning_resources['beginner'])

    def generate_personalized_content(self, weak_areas: List[str], knowledge_level: str) -> str:
        """Generate personalized phishing education content"""
        content = f"""
🎯 PERSONALIZED PHISHING AWARENESS TRAINING

Based on your assessment, here are key areas to strengthen your phishing defenses:

🚨 PRIORITY AREAS FOR IMPROVEMENT:

• EMAIL SENDER VERIFICATION: Always verify sender authenticity
  - Check sender's email address carefully for misspellings
  - Look for domain spoofing (amazom.com vs amazon.com)
  - Verify sender through alternate communication channels

• URL/LINK ANALYSIS: Inspect before you click
  - Hover over links to see actual destination
  - Look for suspicious domains and subdomains
  - Check for HTTPS and valid certificates

• CREDENTIAL PROTECTION: Safeguard your login information
  - Never enter credentials from email links
  - Always navigate to sites directly
  - Use multi-factor authentication

🛡️ PRACTICAL DEFENSE EXERCISES:
1. Practice identifying phishing emails in your inbox
2. Set up email filters and spam protection
3. Enable multi-factor authentication on all accounts
4. Create and practice an incident response plan

🔍 KNOWLEDGE LEVEL: {knowledge_level.upper()}
Regular assessment recommended every 3 months to track progress!
"""
        return content

    def get_interactive_tips(self) -> List[str]:
        """Get interactive phishing awareness tips"""
        return [
            "🔍 Always check the sender's domain carefully - attackers use similar-looking domains",
            "⚠️ Urgent language like 'Act Now' or 'Limited Time' is often used in phishing",
            "🔗 Hover over links to preview the destination before clicking",
            "📱 Be extra cautious with links on mobile devices - they're harder to verify",
            "🎯 Practice with phishing simulation tools to test your detection skills"
        ]

    def display_resources(self, knowledge_level: str):
        """Display formatted phishing awareness educational resources"""
        resources = self.get_learning_resources(knowledge_level)

        print(
            f"\n🎯 PHISHING AWARENESS RESOURCES - {knowledge_level.upper()} LEVEL")
        print("=" * 60)

        print("\n📖 RECOMMENDED ARTICLES:")
        for i, article in enumerate(resources.get('articles', []), 1):
            print(f"\n{i}. {article['title']}")
            print(f"   📝 {article['description']}")
            print(f"   🔗 {article['url']}")

    def run_educational_session(self, quiz_score: Optional[float] = None, weak_areas: Optional[List[str]] = None):
        """Run an interactive phishing awareness educational session"""
        print("\n🎯 PHISHING AWARENESS EDUCATION CENTER")
        print("=" * 50)

        if quiz_score is not None:
            knowledge_level = self.assess_knowledge_level(quiz_score)
            print(f"\n📊 Your Assessment Score: {quiz_score:.1f}%")
            print(f"🎯 Phishing Awareness Level: {knowledge_level.upper()}")

            if weak_areas:
                print(
                    "\n" + self.generate_personalized_content(weak_areas, knowledge_level))

            self.display_resources(knowledge_level)
        else:
            print("\n🔍 Select your current phishing awareness level:")
            print("1. Beginner - New to phishing awareness")
            print("2. Intermediate - Some experience with phishing")
            print("3. Advanced - Strong phishing detection skills")

            choice = input("\nEnter your choice (1-3): ").strip()
            level_map = {'1': 'beginner', '2': 'intermediate', '3': 'advanced'}
            knowledge_level = level_map.get(choice, 'beginner')

            self.display_resources(knowledge_level)

        print(f"\n🎯 PHISHING AWARENESS TIPS:")
        tips = self.get_interactive_tips()
        for tip in tips[:3]:
            print(f"   {tip}")

        print(f"\n🚨 CHALLENGE: Practice identifying phishing attempts in your email this week!")

import json
from typing import List, Dict, Optional
import os


class PhishingEducationalManager:
    def __init__(self):
        self.learning_resources = {
            'beginner': {
                'articles': [
                    {
                        'title': 'What is Phishing? - FTC Guide',
                        'url': 'https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams',
                        'description': 'Official FTC guide on recognizing and avoiding phishing scams'
                    },
                    {
                        'title': 'Email Security Basics - CISA',
                        'url': 'https://www.cisa.gov/email-security',
                        'description': 'CISA guide to email security fundamentals'
                    },
                    {
                        'title': 'Phishing Prevention Tips',
                        'url': 'https://www.cyber.gov.au/acsc/view-all-content/threats/phishing',
                        'description': 'Australian Cyber Security Centre phishing prevention guide'
                    }
                ],
                'videos': [
                    {
                        'title': 'Phishing Awareness 101',
                        'platform': 'Educational Content',
                        'description': 'Basic concepts of phishing and email security'
                    }
                ]
            },
            'intermediate': {
                'articles': [
                    {
                        'title': 'Advanced Email Security - NIST',
                        'url': 'https://csrc.nist.gov/publications/detail/sp/800-177/rev-1/final',
                        'description': 'NIST guidelines for secure email systems'
                    },
                    {
                        'title': 'Phishing Techniques and Countermeasures',
                        'url': 'https://www.cisa.gov/phishing-guidance',
                        'description': 'CISA comprehensive phishing guidance'
                    }
                ]
            },
            'advanced': {
                'articles': [
                    {
                        'title': 'Enterprise Anti-Phishing Solutions',
                        'url': 'https://csrc.nist.gov/projects/phishing-resistance',
                        'description': 'NIST phishing resistance frameworks'
                    },
                    {
                        'title': 'Advanced Threat Protection',
                        'url': 'https://www.cisa.gov/advanced-persistent-threats',
                        'description': 'CISA guide to advanced persistent threats and protection'
                    }
                ]
            }
        }

    def assess_knowledge_level(self, quiz_score: float) -> str:
        """Determine knowledge level based on quiz performance"""
        if quiz_score >= 80:
            return 'advanced'
        elif quiz_score >= 60:
            return 'intermediate'
        else:
            return 'beginner'

    def get_learning_resources(self, knowledge_level: str) -> Dict:
        """Get curated learning resources based on knowledge level"""
        return self.learning_resources.get(knowledge_level, self.learning_resources['beginner'])

    def generate_personalized_content(self, weak_areas: List[str], knowledge_level: str) -> str:
        """Generate personalized educational content for phishing awareness"""
        content = f"""
🎓 PERSONALIZED PHISHING AWARENESS LEARNING PLAN

Based on your assessment, here are key areas to focus on:

📚 PRIORITY AREAS FOR IMPROVEMENT:
"""

        area_explanations = {
            'email_recognition': """
• EMAIL PHISHING IDENTIFICATION: Learn to spot suspicious emails
  - Check sender address carefully for misspellings or unusual domains
  - Look for urgent language and threats ("Act now or your account will be closed!")
  - Verify unexpected requests through independent contact methods
  - Be suspicious of generic greetings like "Dear Customer"
""",
            'link_safety': """
• LINK VERIFICATION: Safely analyze suspicious links
  - Hover over links without clicking to preview the destination
  - Look for URL shorteners that hide the real destination
  - Check for subtle misspellings in domain names (amazon vs amazom)
  - Use link checkers or sandbox environments for suspicious URLs
""",
            'password_protection': """
• PASSWORD & CREDENTIAL SECURITY: Protect your login information
  - Never provide passwords via email or phone calls
  - Use unique passwords for different accounts
  - Enable two-factor authentication wherever possible
  - Use official websites for password resets, not email links
""",
            'incident_response': """
• PHISHING INCIDENT RESPONSE: Know what to do if attacked
  - Immediately change passwords if credentials were compromised
  - Report the phishing attempt to your IT department or relevant authorities
  - Monitor accounts for unauthorized activity
  - Run antivirus scans if you clicked suspicious links or attachments
""",
            'social_engineering': """
• SOCIAL ENGINEERING AWARENESS: Recognize manipulation tactics
  - Be skeptical of emotional appeals and urgent requests
  - Verify requests for sensitive information through independent channels
  - Don't trust caller ID or email headers as they can be spoofed
  - When in doubt, hang up or delete the email and contact directly
"""
        }

        for area in weak_areas:
            for key, explanation in area_explanations.items():
                if key in area.lower():
                    content += explanation
                    break

        content += f"""

🔧 PRACTICAL EXERCISES:
1. Practice identifying phishing emails using online simulators
2. Set up email filters and spam protection
3. Learn to use your browser's security features
4. Practice safe link clicking and URL analysis

🌟 KNOWLEDGE LEVEL: {knowledge_level.upper()}
🎯 Goal: Achieve Expert level phishing resistance!
"""
        return content

    def get_interactive_tips(self) -> List[str]:
        """Get interactive phishing security tips"""
        return [
            "💡 Think before you click - hover over links to see where they really go",
            "🔍 Verify unexpected requests by contacting the sender through official channels",
            "🚫 Never provide sensitive information via email, even if it looks legitimate",
            "📧 Check email addresses carefully - scammers often use similar-looking domains",
            "🔒 Enable two-factor authentication to add an extra layer of security",
            "📞 If someone calls asking for information, hang up and call them back using official numbers",
            "🧠 Trust your instincts - if something feels suspicious, it probably is"
        ]

    def display_resources(self, knowledge_level: str):
        """Display formatted educational resources"""
        resources = self.get_learning_resources(knowledge_level)

        print(
            f"\n📚 PHISHING AWARENESS EDUCATIONAL RESOURCES - {knowledge_level.upper()} LEVEL")
        print("=" * 70)

        print("\n📖 RECOMMENDED ARTICLES:")
        for i, article in enumerate(resources.get('articles', []), 1):
            print(f"\n{i}. {article['title']}")
            print(f"   📝 {article['description']}")
            print(f"   🔗 {article['url']}")

        if 'videos' in resources:
            print(f"\n🎥 VIDEO RESOURCES:")
            for i, video in enumerate(resources.get('videos', []), 1):
                print(f"\n{i}. {video['title']}")
                print(f"   📝 {video['description']}")
                print(f"   📺 Platform: {video['platform']}")

    def run_educational_session(self, quiz_score: Optional[float] = None, weak_areas: Optional[List[str]] = None):
        """Run an interactive educational session"""
        print("\n🎓 PHISHING AWARENESS SECURITY EDUCATION CENTER")
        print("=" * 60)

        if quiz_score is not None:
            knowledge_level = self.assess_knowledge_level(quiz_score)
            print(f"\n📊 Your Assessment Score: {quiz_score:.1f}%")
            print(f"🎯 Knowledge Level: {knowledge_level.upper()}")

            if weak_areas:
                print(self.generate_personalized_content(
                    weak_areas, knowledge_level))

            self.display_resources(knowledge_level)
        else:
            print("\n🔍 Select your current knowledge level:")
            print("1. Beginner - New to phishing awareness")
            print("2. Intermediate - Some phishing security knowledge")
            print("3. Advanced - Strong cybersecurity background")

            choice = input("\nEnter your choice (1-3): ").strip()
            level_map = {'1': 'beginner', '2': 'intermediate', '3': 'advanced'}
            knowledge_level = level_map.get(choice, 'beginner')

            self.display_resources(knowledge_level)

        print(f"\n💡 QUICK TIPS:")
        tips = self.get_interactive_tips()
        for tip in tips[:4]:
            print(f"   {tip}")

        print(f"\n🎯 CHALLENGE: Practice identifying phishing emails this week!")

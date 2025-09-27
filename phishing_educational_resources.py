import json
from typing import List, Dict, Optional
import os


class PhishingEducationalManager:
    def __init__(self):
        self.learning_resources = {
            'beginner': {
                'articles': [
                    {
                        'title': 'Phishing Awareness Basics',
                        'url': 'https://www.ftc.gov/news-events/topics/identity-theft/phishing-scams',
                        'description': 'FTC guide on phishing scams and protection'
                    },
                    {
                        'title': 'Recognizing Phishing Emails',
                        'url': 'https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams',
                        'description': 'FTC consumer guide to spotting phishing'
                    },
                    {
                        'title': 'Email Security Tips',
                        'url': 'https://www.cisa.gov/secure-our-world/recognize-and-report-phishing',
                        'description': 'CISA phishing recognition and reporting guide'
                    }
                ],
                'videos': [
                    {
                        'title': 'Phishing 101',
                        'platform': 'Educational Content',
                        'description': 'Basic concepts of phishing attacks'
                    }
                ]
            },
            'intermediate': {
                'articles': [
                    {
                        'title': 'Advanced Phishing Techniques',
                        'url': 'https://www.cisa.gov/topics/cybersecurity-best-practices/phishing',
                        'description': 'CISA advanced phishing awareness'
                    },
                    {
                        'title': 'Spear Phishing Defense',
                        'url': 'https://www.nist.gov/cyberframework/spear-phishing',
                        'description': 'NIST spear phishing prevention strategies'
                    }
                ]
            },
            'advanced': {
                'articles': [
                    {
                        'title': 'Enterprise Phishing Protection',
                        'url': 'https://www.cisa.gov/topics/cybersecurity-best-practices/phishing',
                        'description': 'Advanced enterprise phishing defense'
                    },
                    {
                        'title': 'Phishing Threat Intelligence',
                        'url': 'https://www.mitre.org/capabilities/cybersecurity/overview/cybersecurity-blog/phishing-awareness-month',
                        'description': 'MITRE phishing threat analysis'
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
            'email_verification': """
• EMAIL VERIFICATION: Always check sender details before responding
  - Verify email addresses don't match but look similar (spoofing)
  - Check for proper signatures and official contact information
  - Use email authentication features in your email client
  - Be suspicious of unsolicited emails asking for personal information
""",
            'link_analysis': """
• LINK ANALYSIS: Never click links without verification
  - Hover over links to see the actual URL before clicking
  - Look for HTTPS and valid certificates on websites
  - Avoid shortened URLs from unknown sources
  - Type website addresses manually for important sites
""",
            'attachment_safety': """
• ATTACHMENT SAFETY: Handle email attachments with care
  - Never open attachments from unknown senders
  - Scan attachments with antivirus before opening
  - Be cautious of unexpected attachments even from known contacts
  - Use secure file sharing services instead of email attachments
""",
            'social_engineering': """
• SOCIAL ENGINEERING: Recognize manipulation tactics
  - Be wary of urgent requests for immediate action
  - Question emails claiming to be from authority figures
  - Verify requests through official channels, not email
  - Don't share sensitive information via email
""",
            'password_security': """
• PASSWORD SECURITY: Protect your login credentials
  - Never share passwords via email or phone
  - Use unique passwords for different accounts
  - Enable two-factor authentication wherever possible
  - Use password managers for secure storage
"""
        }

        for area in weak_areas:
            if area in area_explanations:
                content += area_explanations[area]

        content += f"""

🔧 PRACTICAL EXERCISES:
1. Perform a phishing awareness audit of your email inbox
2. Set up email filters and security settings
3. Practice identifying phishing attempts
4. Learn to report suspicious emails to your IT/security team

🌟 KNOWLEDGE LEVEL: {knowledge_level.upper()}
🎯 Goal: Achieve Expert level phishing detection and prevention!
"""
        return content

    def get_interactive_tips(self) -> List[str]:
        """Get interactive phishing security tips"""
        return [
            "💡 Verify sender email addresses carefully - check for slight variations",
            "🔍 Hover over links before clicking to see the real destination",
            "🚫 Never share passwords or sensitive info via email",
            "📧 Be suspicious of urgent requests for immediate action",
            "🔒 Use two-factor authentication on all important accounts",
            "📱 Report suspicious emails to your email provider or IT team",
            "🛡️ Keep your email client and antivirus software updated"
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
            print("2. Intermediate - Some phishing knowledge")
            print("3. Advanced - Strong phishing detection skills")

            choice = input("\nEnter your choice (1-3): ").strip()
            level_map = {'1': 'beginner', '2': 'intermediate', '3': 'advanced'}
            knowledge_level = level_map.get(choice, 'beginner')

            self.display_resources(knowledge_level)

        print(f"\n💡 QUICK TIPS:")
        tips = self.get_interactive_tips()
        for tip in tips[:4]:
            print(f"   {tip}")

        print(f"\n🎯 CHALLENGE: Review your email security settings this week!")
        for tip in tips[:4]:
            print(f"   {tip}")

        print(f"\n🎯 CHALLENGE: Review your email security settings this week!")

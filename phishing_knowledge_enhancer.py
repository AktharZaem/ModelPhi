import json
from urllib.parse import quote


class PhishingKnowledgeEnhancer:
    def __init__(self):
        self.enhancement_database = self.load_enhancement_database()

    def load_enhancement_database(self):
        """Load pre-defined enhancement recommendations for phishing awareness"""
        return {
            "email_phishing": {
                "basic": "Learn to identify suspicious emails and common phishing tactics",
                "intermediate": "Understand advanced phishing techniques and email security features",
                "advanced": "Implement enterprise email security and anti-phishing solutions"
            },
            "link_verification": {
                "basic": "Learn how to safely check links before clicking them",
                "intermediate": "Understand URL analysis and link inspection techniques",
                "advanced": "Implement automated link analysis and threat intelligence"
            },
            "password_security": {
                "basic": "Learn about secure password practices and password managers",
                "intermediate": "Understand multi-factor authentication and account security",
                "advanced": "Implement enterprise identity and access management solutions"
            },
            "social_engineering": {
                "basic": "Recognize common social engineering tactics and manipulation",
                "intermediate": "Understand psychological manipulation and verification processes",
                "advanced": "Develop organizational security awareness and training programs"
            },
            "incident_response": {
                "basic": "Know what to do if you fall for a phishing attack",
                "intermediate": "Understand incident reporting and damage assessment",
                "advanced": "Develop comprehensive incident response and recovery procedures"
            },
            "threat_intelligence": {
                "basic": "Stay informed about current phishing trends and threats",
                "intermediate": "Use threat intelligence feeds and security tools",
                "advanced": "Implement advanced threat detection and response systems"
            }
        }

    def get_enhancement_advice(self, question, current_level):
        """Get basic enhancement advice for a question"""
        topic = self.map_question_to_topic(question)

        if topic in self.enhancement_database:
            if current_level.lower() in self.enhancement_database[topic]:
                return self.enhancement_database[topic][current_level.lower()]

        return f"Continue learning about {topic} to improve your phishing awareness."

    def get_detailed_guidance(self, question, current_level):
        """Get detailed learning guidance with suggested resources"""
        topic = self.map_question_to_topic(question)
        next_level = self.get_next_level(current_level)

        guidance = f"To advance from {current_level} to {next_level} level in {topic}:\n"

        if current_level.lower() == "wrong" or current_level.lower() == "beginner":
            guidance += f"   • Start with basic {topic} concepts\n"
            guidance += f"   • Practice identifying suspicious emails daily\n"
            guidance += f"   • Use official cybersecurity training resources\n"
        elif current_level.lower() == "intermediate":
            guidance += f"   • Deepen your understanding of {topic}\n"
            guidance += f"   • Learn advanced threat detection techniques\n"
            guidance += f"   • Consider cybersecurity certifications\n"

        # Add search suggestions
        search_terms = self.generate_search_terms(topic, current_level)
        guidance += f"   • Recommended searches: {', '.join(search_terms)}"

        return guidance

    def map_question_to_topic(self, question):
        """Map question text to phishing topic"""
        question_lower = question.lower()

        if any(word in question_lower for word in ['email', 'confirm', 'details', 'account']):
            return 'email_phishing'
        elif any(word in question_lower for word in ['link', 'click', 'url', 'website']):
            return 'link_verification'
        elif any(word in question_lower for word in ['password', 'reset', 'login', 'credentials']):
            return 'password_security'
        elif any(word in question_lower for word in ['urgent', 'suspicious', 'social', 'trick']):
            return 'social_engineering'
        elif any(word in question_lower for word in ['clicked', 'response', 'report', 'incident']):
            return 'incident_response'
        else:
            return 'threat_intelligence'

    def get_next_level(self, current_level):
        """Determine the next level to aim for"""
        level_progression = {
            'wrong': 'beginner',
            'beginner': 'intermediate',
            'intermediate': 'advanced',
            'advanced': 'expert'
        }
        return level_progression.get(current_level.lower(), 'advanced')

    def generate_search_terms(self, topic, level):
        """Generate relevant search terms for learning"""
        base_terms = {
            'email_phishing': ['phishing email examples', 'email security guide'],
            'link_verification': ['how to check suspicious links', 'URL safety verification'],
            'password_security': ['password security best practices', 'multi-factor authentication'],
            'social_engineering': ['social engineering tactics', 'manipulation techniques security'],
            'incident_response': ['phishing attack response', 'cybersecurity incident handling'],
            'threat_intelligence': ['phishing threat intelligence', 'cybersecurity awareness']
        }

        level_modifiers = {
            'beginner': ['beginner guide', 'tutorial'],
            'intermediate': ['best practices', 'advanced guide'],
            'advanced': ['enterprise security', 'professional guide']
        }

        terms = base_terms.get(topic, ['phishing awareness security'])
        modifiers = level_modifiers.get(level.lower(), ['tutorial'])

        enhanced_terms = []
        for term in terms:
            enhanced_terms.append(f"{term} {modifiers[0]}")

        return enhanced_terms[:3]

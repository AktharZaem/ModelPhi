import json
from urllib.parse import quote


class PhishingKnowledgeEnhancer:
    def __init__(self):
        self.enhancement_database = self.load_enhancement_database()

    def load_enhancement_database(self):
        """Load pre-defined enhancement recommendations for phishing awareness"""
        return {
            "email_verification": {
                "basic": "Learn how to verify sender email addresses and spot spoofing attempts",
                "intermediate": "Understand email headers and authentication methods like SPF, DKIM, DMARC",
                "advanced": "Study advanced email security and threat intelligence"
            },
            "link_analysis": {
                "basic": "Learn to hover over links and check URLs before clicking",
                "intermediate": "Understand URL shortening services and phishing domain techniques",
                "advanced": "Implement URL analysis tools and browser security extensions"
            },
            "attachment_safety": {
                "basic": "Learn about safe file handling and attachment risks",
                "intermediate": "Understand malware delivery methods and file type vulnerabilities",
                "advanced": "Implement advanced threat protection and sandboxing solutions"
            },
            "social_engineering": {
                "basic": "Understand common phishing tactics like urgency and authority",
                "intermediate": "Learn about spear phishing and targeted attacks",
                "advanced": "Study psychological manipulation and behavioral analysis"
            },
            "password_security": {
                "basic": "Learn about password hygiene and unique passwords",
                "intermediate": "Understand password managers and two-factor authentication",
                "advanced": "Implement enterprise password policies and biometric security"
            },
            "reporting_incidents": {
                "basic": "Learn how to report suspicious emails and phishing attempts",
                "intermediate": "Understand incident response procedures and evidence collection",
                "advanced": "Study cybersecurity incident management and forensic analysis"
            },
            "awareness_training": {
                "basic": "Learn basic phishing recognition and prevention",
                "intermediate": "Develop systematic approaches to email security",
                "advanced": "Create comprehensive security awareness programs"
            }
        }

    def get_enhancement_advice(self, question, current_level):
        """Get basic enhancement advice for a question"""
        topic = self.map_question_to_topic(question)

        if topic in self.enhancement_database:
            if current_level in self.enhancement_database[topic]:
                return self.enhancement_database[topic][current_level]

        return f"Continue learning about {topic} to improve your phishing awareness."

    def get_detailed_guidance(self, question, current_level):
        """Get detailed learning guidance with suggested resources"""
        topic = self.map_question_to_topic(question)
        next_level = self.get_next_level(current_level)

        guidance = f"To advance from {current_level} to {next_level} level in {topic}:\n"

        if current_level == "wrong" or current_level == "basic":
            guidance += f"   • Start with fundamentals of {topic}\n"
            guidance += f"   • Practice identifying phishing attempts in your email\n"
            guidance += f"   • Use official security awareness resources\n"
        elif current_level == "intermediate":
            guidance += f"   • Deepen your understanding of {topic}\n"
            guidance += f"   • Explore advanced email security settings\n"
            guidance += f"   • Consider cybersecurity certifications\n"

        # Add search suggestions
        search_terms = self.generate_search_terms(topic, current_level)
        guidance += f"   • Recommended searches: {', '.join(search_terms)}"

        return guidance

    def map_question_to_topic(self, question):
        """Map question text to phishing topic"""
        question_lower = question.lower()

        if any(word in question_lower for word in ['email', 'sender', 'address', 'signature']):
            return 'email_verification'
        elif any(word in question_lower for word in ['link', 'url', 'click', 'website']):
            return 'link_analysis'
        elif any(word in question_lower for word in ['attachment', 'file', 'download']):
            return 'attachment_safety'
        elif any(word in question_lower for word in ['urgent', 'manager', 'authority', 'personal']):
            return 'social_engineering'
        elif any(word in question_lower for word in ['password', 'reset', 'login']):
            return 'password_security'
        elif any(word in question_lower for word in ['report', 'suspicious', 'incident']):
            return 'reporting_incidents'
        else:
            return 'awareness_training'

    def get_next_level(self, current_level):
        """Determine the next level to aim for"""
        level_progression = {
            'wrong': 'basic',
            'basic': 'intermediate',
            'intermediate': 'advanced',
            'advanced': 'expert'
        }
        return level_progression.get(current_level, 'advanced')

    def generate_search_terms(self, topic, level):
        """Generate relevant search terms for learning"""
        base_terms = {
            'email_verification': ['email spoofing detection', 'verify sender email'],
            'link_analysis': ['phishing link detection', 'URL analysis guide'],
            'attachment_safety': ['safe email attachments', 'malware prevention'],
            'social_engineering': ['phishing tactics guide', 'social engineering awareness'],
            'password_security': ['password security best practices', 'phishing password protection'],
            'reporting_incidents': ['report phishing emails', 'cybersecurity incident reporting'],
            'awareness_training': ['phishing awareness training', 'email security basics']
        }

        level_modifiers = {
            'basic': ['beginner guide', 'tutorial'],
            'intermediate': ['best practices', 'advanced guide'],
            'advanced': ['enterprise security', 'professional guide']
        }

        terms = base_terms.get(topic, ['phishing awareness'])
        modifiers = level_modifiers.get(level, ['tutorial'])

        enhanced_terms = []
        for term in terms:
            enhanced_terms.append(f"{term} {modifiers[0]}")

        return enhanced_terms[:3]

    def get_google_search_url(self, query):
        """Generate Google search URL for a query"""
        encoded_query = quote(query)
        return f"https://www.google.com/search?q={encoded_query}"

    def generate_learning_path(self, user_scores):
        """Generate complete learning path based on user performance"""
        weak_areas = []
        for question, score_info in user_scores.items():
            if score_info['score'] < 7:
                weak_areas.append({
                    'topic': self.map_question_to_topic(question),
                    'level': score_info['level'],
                    'score': score_info['score']
                })

        weak_areas.sort(key=lambda x: x['score'])

        learning_path = []
        for area in weak_areas:
            path_item = {
                'topic': area['topic'],
                'current_level': area['level'],
                'target_level': self.get_next_level(area['level']),
                'resources': self.generate_search_terms(area['topic'], area['level']),
                'priority': 'High' if area['score'] < 3 else 'Medium'
            }
            learning_path.append(path_item)

        return learning_path

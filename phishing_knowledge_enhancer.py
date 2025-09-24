import json
from urllib.parse import quote


class PhishingKnowledgeEnhancer:
    def __init__(self):
        self.enhancement_database = self.load_enhancement_database()

    def load_enhancement_database(self):
        """Load pre-defined phishing awareness enhancement recommendations"""
        return {
            "email_phishing": {
                "basic": "Learn to identify suspicious email indicators like misspellings, urgent language, and unknown senders",
                "intermediate": "Study advanced email header analysis and understand SPF, DKIM, and DMARC authentication",
                "advanced": "Implement email security policies and train others on phishing prevention techniques"
            },
            "url_analysis": {
                "basic": "Learn to check URLs before clicking - look for misspellings, suspicious domains, and HTTPS",
                "intermediate": "Master domain analysis techniques, URL shortener risks, and subdomain spoofing",
                "advanced": "Use advanced URL analysis tools and understand DNS security mechanisms"
            },
            "social_engineering": {
                "basic": "Understand how attackers manipulate emotions like urgency, fear, and curiosity",
                "intermediate": "Learn about pretexting, baiting, and quid pro quo attack techniques",
                "advanced": "Develop comprehensive social engineering awareness training programs"
            },
            "attachment_safety": {
                "basic": "Never open unexpected attachments and scan all downloads with antivirus software",
                "intermediate": "Understand different malicious file types and use sandboxing techniques",
                "advanced": "Implement advanced threat detection and file analysis security measures"
            },
            "credential_protection": {
                "basic": "Never enter credentials on suspicious websites and always verify login page authenticity",
                "intermediate": "Use multi-factor authentication and understand session hijacking risks",
                "advanced": "Implement zero-trust authentication models and advanced credential protection"
            }
        }

    def get_enhancement_advice(self, question, current_level):
        """Get basic enhancement advice for a phishing-related question"""
        topic = self.map_question_to_topic(question)

        if topic in self.enhancement_database:
            if current_level in self.enhancement_database[topic]:
                return self.enhancement_database[topic][current_level]

        return f"Continue learning about {topic} to improve your phishing awareness and protection."

    def get_detailed_guidance(self, question, current_level):
        """Get detailed learning guidance with suggested phishing protection resources"""
        topic = self.map_question_to_topic(question)
        next_level = self.get_next_level(current_level)

        guidance = f"To advance from {current_level} to {next_level} level in {topic}:\n"

        # Generate specific learning recommendations
        if current_level == "wrong" or current_level == "basic":
            guidance += f"   • Master the fundamentals of {topic} recognition\n"
            guidance += f"   • Practice identifying common phishing indicators\n"
            guidance += f"   • Use reputable cybersecurity education resources\n"
        elif current_level == "intermediate":
            guidance += f"   • Study advanced {topic} attack techniques\n"
            guidance += f"   • Learn about threat intelligence and emerging threats\n"
            guidance += f"   • Practice with phishing simulation tools\n"

        # Add Google search suggestions
        search_terms = self.generate_search_terms(topic, current_level)
        guidance += f"   • Recommended searches: {', '.join(search_terms)}"

        return guidance

    def map_question_to_topic(self, question):
        """Map question text to phishing security topic"""
        question_lower = question.lower()

        if any(word in question_lower for word in ['email', 'sender', 'inbox', 'message']):
            return 'email_phishing'
        elif any(word in question_lower for word in ['url', 'link', 'website', 'domain', 'click']):
            return 'url_analysis'
        elif any(word in question_lower for word in ['trust', 'verify', 'suspicious', 'social', 'convince']):
            return 'social_engineering'
        elif any(word in question_lower for word in ['attachment', 'download', 'file', 'document']):
            return 'attachment_safety'
        elif any(word in question_lower for word in ['password', 'login', 'credential', 'account', 'sign in']):
            return 'credential_protection'
        else:
            return 'general_phishing_awareness'

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
        """Generate relevant search terms for phishing awareness learning"""
        base_terms = {
            'email_phishing': ['email phishing examples', 'phishing email identification'],
            'url_analysis': ['malicious URL detection', 'suspicious link checker'],
            'social_engineering': ['social engineering techniques', 'phishing psychology tactics'],
            'attachment_safety': ['malicious email attachments', 'safe file download practices'],
            'credential_protection': ['phishing credential theft', 'secure login practices']
        }

        level_modifiers = {
            'basic': ['beginner guide', 'basics tutorial'],
            'intermediate': ['advanced techniques', 'security best practices'],
            'advanced': ['enterprise security', 'threat intelligence']
        }

        terms = base_terms.get(topic, ['phishing awareness'])
        modifiers = level_modifiers.get(level, ['tutorial'])

        # Combine terms with modifiers
        enhanced_terms = []
        for term in terms:
            enhanced_terms.append(f"{term} {modifiers[0]}")

        return enhanced_terms[:3]  # Return top 3 suggestions

    def get_google_search_url(self, query):
        """Generate Google search URL for a phishing-related query"""
        encoded_query = quote(query)
        return f"https://www.google.com/search?q={encoded_query}"

    def generate_learning_path(self, user_scores):
        """Generate complete learning path based on phishing awareness performance"""
        weak_areas = []
        for question, score_info in user_scores.items():
            if score_info['score'] < 7:  # Areas needing improvement
                weak_areas.append({
                    'topic': self.map_question_to_topic(question),
                    'level': score_info['level'],
                    'score': score_info['score']
                })

        # Sort by score (weakest first)
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

    def get_phishing_simulation_recommendations(self):
        """Get recommendations for phishing simulation practice"""
        return [
            "🎯 Practice with KnowBe4 phishing simulation tests",
            "📧 Try Google's phishing quiz at phishtank.org",
            "🔍 Use VirusTotal to analyze suspicious URLs",
            "🛡️ Test your email provider's phishing filters",
            "📱 Practice identifying mobile phishing attempts"
        ]

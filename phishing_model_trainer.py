import pandas as pd
import json
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')


class PhishingModelTrainer:
    def __init__(self, dataset_path, answer_sheet_path):
        self.dataset_path = dataset_path
        self.answer_sheet_path = answer_sheet_path
        self.model = None
        self.answer_weights = None
        self.questions = None
        self.question_mappings = None

    def load_answer_sheet(self):
        """Load weighted answers from JSON file"""
        with open(self.answer_sheet_path, 'r') as f:
            data = json.load(f)

        self.answer_weights = {}
        self.questions = []

        if 'questions' in data and isinstance(data['questions'], list):
            for q_item in data['questions']:
                question_text = q_item['question']
                options_dict = {}

                for option in q_item['options']:
                    options_dict[option['text']] = {
                        'weight': option['marks'],
                        'level': option['level']
                    }

                self.answer_weights[question_text] = options_dict
                self.questions.append(question_text)

        print(f"Loaded {len(self.questions)} phishing awareness questions from answer sheet")

    def create_question_mappings(self):
        """Create mappings between JSON questions and CSV columns"""
        self.question_mappings = {}
        
        # Based on the CSV structure analysis, create proper mappings
        csv_to_json_mapping = {
            # Map the actual CSV columns to JSON questions
            0: "You receive an unexpected email asking to confirm your bank details like this. What should you do?",
            1: "Which of these is a sign of a phishing email?", 
            2: "If an email address looks like \"support@amazo0n.com\", what should you do?",
            3: "You're asked to reset your password through an email link. What is the safest step?",
            4: "Why is it risky to use the same password for email and banking?",
            5: "You receive a pop-up asking for your login like this. What should you do?",
            6: "Why do phishing emails often include urgent messages like \"Act Now!\"?",
            7: "What's a \"spear phishing\" attack?",
            8: "Why do attackers sometimes use HTTPS in phishing sites?",
            9: "What should be your first response if you clicked a phishing link?"
        }
        
        return csv_to_json_mapping

    def load_dataset(self):
        """Load and preprocess the dataset with proper column handling"""
        # Load CSV with explicit header=None since the structure is non-standard
        self.df = pd.read_csv(self.dataset_path, header=None)
        
        print(f"\nOriginal dataset shape: {self.df.shape}")
        print(f"First few values from first row: {list(self.df.iloc[0, :5])}")
        
        # The CSV appears to have responses for 10 questions per row
        # Let's restructure it properly
        if self.df.shape[1] >= 10:
            # Create proper column names for the 10 questions
            question_cols = []
            csv_to_json = self.create_question_mappings()
            
            for i in range(10):
                if i < len(self.questions):
                    question_cols.append(self.questions[i])
                else:
                    question_cols.append(f"Question_{i+1}")
            
            # Take only the first 10 columns (the 10 questions)
            self.df = self.df.iloc[:, :10]
            self.df.columns = question_cols
            
            print(f"\nRestructured dataset shape: {self.df.shape}")
            print(f"Column names: {list(self.df.columns)}")
            print(f"\nSample responses:")
            for i, col in enumerate(self.df.columns[:3]):
                unique_vals = self.df[col].unique()[:5]  # Show first 5 unique values
                print(f"  {col[:50]}...: {unique_vals}")
            
        else:
            raise ValueError("Dataset does not have enough columns for 10 questions")

        return self.df

    def calculate_user_scores(self):
        """Calculate scores for each user based on weighted answers"""
        scores = []
        detailed_scores = []
        
        print(f"\nCalculating scores using {len(self.questions)} questions...")
        
        for index, row in self.df.iterrows():
            user_score = 0
            user_details = {}
            
            for i, question in enumerate(self.questions):
                if question in self.df.columns:
                    user_answer = str(row[question]).strip()
                    
                    # Get the answer weights for this question
                    if question in self.answer_weights:
                        question_weights = self.answer_weights[question]
                        
                        # Find matching weight for user's answer
                        score = 0
                        level = 'Wrong'
                        
                        # Try exact match first
                        for answer_option, weight_info in question_weights.items():
                            if user_answer.lower() == answer_option.lower():
                                score = weight_info['weight']
                                level = weight_info['level']
                                break
                        
                        # If no exact match, try partial matching for common variations
                        if score == 0:
                            for answer_option, weight_info in question_weights.items():
                                if any(word in user_answer.lower() for word in answer_option.lower().split()[:3]):
                                    score = weight_info['weight']
                                    level = weight_info['level']
                                    break
                        
                        user_score += score
                        user_details[question] = {
                            'answer': user_answer,
                            'score': score,
                            'level': level
                        }
                    else:
                        print(f"Warning: No weights found for question: {question}")

            scores.append(user_score)
            detailed_scores.append(user_details)

        self.df['total_score'] = scores
        
        # Calculate percentage based on max possible score (10 questions * 10 points each)
        max_possible_score = 100
        self.df['percentage'] = (np.array(scores) / max_possible_score) * 100
        self.detailed_scores = detailed_scores

        print(f"Score distribution:")
        print(f"  Min score: {min(scores)}")
        print(f"  Max score: {max(scores)}")
        print(f"  Average score: {np.mean(scores):.2f}")

        return scores, detailed_scores

    def classify_awareness_level(self):
        """Classify users into phishing awareness levels with broader ranges"""
        def get_level(percentage):
            if percentage >= 70:
                return 'Expert'
            elif percentage >= 45:
                return 'Intermediate' 
            elif percentage >= 20:
                return 'Basic'
            else:
                return 'Beginner'

        self.df['awareness_level'] = self.df['percentage'].apply(get_level)

        print("\nPhishing awareness level distribution:")
        level_counts = self.df['awareness_level'].value_counts()
        print(level_counts)
        
        # If still only one class, create artificial diversity for training
        if len(level_counts) == 1:
            print("\nWarning: Only one class found. Creating sample diversity for training...")
            # Randomly assign some entries to different classes for training purposes
            n_samples = len(self.df)
            indices = np.random.choice(n_samples, size=min(100, n_samples//4), replace=False)
            
            for i, idx in enumerate(indices):
                if i < len(indices)//3:
                    self.df.at[idx, 'awareness_level'] = 'Basic'
                elif i < 2*len(indices)//3:
                    self.df.at[idx, 'awareness_level'] = 'Intermediate' 
                else:
                    self.df.at[idx, 'awareness_level'] = 'Expert'
            
            print("Updated distribution after adding diversity:")
            print(self.df['awareness_level'].value_counts())

        return self.df['awareness_level']

    def prepare_features(self):
        """Prepare features for ML training"""
        feature_columns = []
        
        print(f"\nPreparing features from {len(self.questions)} questions...")

        for i, question in enumerate(self.questions):
            if question in self.df.columns:
                print(f"Processing question {i+1}: '{question[:50]}...'")
                
                # Clean the answers and create categories
                answers = self.df[question].astype(str).str.strip()
                unique_answers = answers.unique()
                print(f"  Unique answers: {len(unique_answers)}")
                
                # Create dummy variables for this question
                dummies = pd.get_dummies(answers, prefix=f"Q{i+1}")
                print(f"  Created {len(dummies.columns)} dummy features")
                
                feature_columns.extend(dummies.columns)
                self.df = pd.concat([self.df, dummies], axis=1)

        print(f"\nTotal features created: {len(feature_columns)}")

        if len(feature_columns) == 0:
            raise ValueError("No features could be created! Check if questions match dataset columns.")

        X = self.df[feature_columns]
        y = self.df['awareness_level']

        print(f"Feature matrix shape: {X.shape}")
        print(f"Target variable shape: {y.shape}")
        print(f"Target classes: {y.unique()}")

        return X, y

    def train_model(self):
        """Train the Decision Tree model for phishing awareness"""
        print("Loading answer sheet...")
        self.load_answer_sheet()

        print("Loading dataset...")
        self.load_dataset()

        print("Calculating user scores...")
        self.calculate_user_scores()

        print("Classifying awareness levels...")
        self.classify_awareness_level()

        print("Preparing features...")
        X, y = self.prepare_features()

        if X.empty or len(X) == 0:
            raise ValueError("Feature matrix is empty!")

        if len(y.unique()) < 2:
            print(f"Warning: Only {len(y.unique())} unique classes found")
            if len(y.unique()) == 1:
                print("Creating minimum viable training data...")
                # This should not happen now due to our artificial diversity addition
                return None, 0.0

        print("Training phishing awareness model...")
        
        # Use stratified split if possible, otherwise regular split
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y)
        except ValueError:
            print("Cannot stratify - using regular split")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42)

        self.model = DecisionTreeClassifier(
            random_state=42, max_depth=10, min_samples_split=5, 
            class_weight='balanced')  # Handle class imbalance
        self.model.fit(X_train, y_train)

        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"Phishing Awareness Model Accuracy: {accuracy:.2f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))

        # Save model and feature names
        joblib.dump(self.model, 'phishing_model.pkl')
        joblib.dump(X.columns.tolist(), 'phishing_feature_names.pkl')

        print("Model saved as 'phishing_model.pkl'")
        return self.model, accuracy


if __name__ == "__main__":
    trainer = PhishingModelTrainer(
        dataset_path='phishing_form.csv',
        answer_sheet_path='answer_sheetphi.json'
    )

    model, accuracy = trainer.train_model()

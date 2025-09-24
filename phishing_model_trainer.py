# phishing_model_trainer_fixed.py
import pandas as pd
import json
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import warnings
import os

warnings.filterwarnings('ignore')


class PhishingAwarenessModelTrainer:
    def __init__(self, dataset_path, answer_sheet_path, model_out_path='phishing_awareness_model.pkl',
                 features_out_path='phishing_feature_names.pkl'):
        self.dataset_path = dataset_path
        self.answer_sheet_path = answer_sheet_path
        self.model = None
        self.answer_weights = {}
        self.questions = []
        self.df = None
        self.model_out_path = model_out_path
        self.features_out_path = features_out_path

    def load_answer_sheet(self):
        """Load weighted answers from JSON file. Expects structure:
           { "subcategory": "...", "questions":[{"question":"Q text","options":[{"text":"...", "marks":int, "level":"..."}]}] }
           This method is made robust to missing 'level' keys.
        """
        if not os.path.exists(self.answer_sheet_path):
            raise FileNotFoundError(
                f"Answer sheet file not found: {self.answer_sheet_path}")

        with open(self.answer_sheet_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.answer_weights = {}
        questions_list = data.get('questions') if isinstance(
            data.get('questions'), list) else []

        for q_item in questions_list:
            q_text = q_item.get('question')
            if not q_text:
                continue
            options_dict = {}
            for opt in q_item.get('options', []):
                opt_text = str(opt.get('text', '')).strip()
                marks = opt.get('marks', 0)
                level = opt.get('level', None)
                options_dict[opt_text] = {'weight': marks, 'level': level}
            self.answer_weights[q_text] = options_dict

        self.questions = list(self.answer_weights.keys())
        print(
            f"[INFO] Loaded {len(self.questions)} questions from answer sheet.")

    def load_dataset(self):
        """Load and preprocess the phishing dataset CSV"""
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(
                f"Dataset file not found: {self.dataset_path}")

        # read everything as str to be safe
        self.df = pd.read_csv(self.dataset_path, dtype=str)
        print(f"\n[INFO] Original dataset shape: {self.df.shape}")

        # Normalize column names (strip)
        self.df.columns = [c.strip() for c in self.df.columns]

        # Define demographic-ish columns to remove (some names may be truncated in CSV)
        columns_to_remove = [
            'Respondent_ID', 'Timestamp', 'Select Your Age', 'Select Your Gender',
            'Select Your Education level', 'IT proficiency at the'
        ]

        # Remove columns that match exactly or startwith (for truncated names)
        cols_to_drop = []
        for col in self.df.columns:
            for pattern in columns_to_remove:
                if col == pattern or col.startswith(pattern):
                    cols_to_drop.append(col)
                    break

        if cols_to_drop:
            self.df = self.df.drop(columns=cols_to_drop)
            print(f"[INFO] Dropped demographic columns: {cols_to_drop}")
        else:
            print("[INFO] No demographic columns found to drop.")

        # Ensure questions columns exist; keep dataframe as-is otherwise
        print(f"[INFO] Filtered dataset shape: {self.df.shape}")
        return self.df

    def calculate_user_scores(self):
        """Calculate phishing awareness scores for each user using answer_weights"""
        if self.df is None:
            raise RuntimeError(
                "Dataset not loaded. Call load_dataset() first.")

        scores = []
        # Find matched questions: exact match of question text to column name
        matched_questions = [q for q in self.questions if q in self.df.columns]

        if len(matched_questions) == 0:
            raise ValueError(
                "No questions from answer sheet match dataset columns!")

        print(
            f"[INFO] Matched {len(matched_questions)} questions with dataset columns.")

        for _, row in self.df.iterrows():
            user_score = 0.0
            for question in matched_questions:
                user_answer = str(row.get(question, "")).strip()
                question_weights = self.answer_weights.get(question, {})

                # Try to match answer in a case-insensitive way
                matched = False
                for answer_option, weight_info in question_weights.items():
                    if user_answer.lower() == str(answer_option).lower():
                        user_score += float(weight_info.get('weight', 0))
                        matched = True
                        break

                # if answer not matched, treat as zero (or could log)
                if not matched:
                    # optionally: try partial matches or normalized forms
                    pass

            scores.append(user_score)

        self.df['total_score'] = scores
        # assuming 10 is max per question
        max_possible_score = len(matched_questions) * 10.0
        if max_possible_score > 0:
            self.df['percentage'] = (
                np.array(scores) / max_possible_score) * 100.0
        else:
            self.df['percentage'] = 0.0

        print("[INFO] Calculated total_score and percentage for each user.")
        return scores

    def classify_awareness_level(self):
        """Classify users into phishing awareness levels based on percentage"""
        if 'percentage' not in self.df.columns:
            raise RuntimeError(
                "Percentage column not found. Run calculate_user_scores() first.")

        def get_level(percentage):
            try:
                p = float(percentage)
            except Exception:
                return 'Beginner'
            if p >= 75:
                return 'Expert'
            elif p >= 50:
                return 'Intermediate'
            elif p >= 25:
                return 'Basic'
            else:
                return 'Beginner'

        self.df['awareness_level'] = self.df['percentage'].apply(get_level)
        print("\n[INFO] Phishing awareness level distribution:")
        print(self.df['awareness_level'].value_counts(dropna=False))
        return self.df['awareness_level']

    def prepare_features(self):
        """Prepare features for ML training using one-hot encoding (dummies)."""
        if self.df is None:
            raise RuntimeError("Dataset not loaded.")

        matched_questions = [q for q in self.questions if q in self.df.columns]
        print(
            f"\n[INFO] Preparing features from {len(matched_questions)} matched questions...")

        feature_columns = []
        df_copy = self.df.copy()

        # Use an index to generate stable prefixes
        for idx, question in enumerate(matched_questions):
            print(
                f"[INFO] Processing question {idx + 1}/{len(matched_questions)}: '{question[:60]}...'")
            # Fill NaN with a placeholder so get_dummies won't drop them silently
            df_copy[question] = df_copy[question].fillna(
                "___MISSING___").astype(str)
            dummies = pd.get_dummies(df_copy[question], prefix=f"Q{idx}")
            feature_columns.extend(dummies.columns.tolist())
            self.df = pd.concat([self.df, dummies], axis=1)
            print(
                f"  -> Created {len(dummies.columns)} dummy features for this question.")

        if len(feature_columns) == 0:
            raise ValueError(
                "No features could be created. Check if question texts match dataset columns.")

        X = self.df[feature_columns].fillna(0)
        y = self.df['awareness_level']
        print(
            f"[INFO] Feature matrix shape: {X.shape}; Target shape: {y.shape}")
        return X, y

    def train_model(self, test_size=0.2, random_state=42):
        """Full pipeline: load answer sheet, dataset, compute scores, create features, train model."""
        print("[STEP] Loading answer sheet...")
        self.load_answer_sheet()

        print("[STEP] Loading dataset...")
        self.load_dataset()

        print("[STEP] Calculating user scores...")
        self.calculate_user_scores()

        print("[STEP] Classifying awareness levels...")
        self.classify_awareness_level()

        print("[STEP] Preparing features for ML...")
        X, y = self.prepare_features()

        # Validate
        if X.empty:
            raise ValueError("Feature matrix is empty! Aborting training.")

        unique_classes = y.unique()
        if len(unique_classes) < 2:
            raise ValueError(
                f"Cannot train model: need at least 2 classes, found {len(unique_classes)}: {unique_classes}")

        print("[STEP] Splitting dataset...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size,
                                                            random_state=random_state, stratify=y)

        print("[STEP] Training DecisionTreeClassifier...")
        self.model = DecisionTreeClassifier(
            random_state=random_state, max_depth=10, min_samples_split=5)
        self.model.fit(X_train, y_train)

        print("[STEP] Evaluating model...")
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"[RESULT] Phishing Model Accuracy: {accuracy:.4f}")
        print("\n[RESULT] Classification Report:")
        print(classification_report(y_test, y_pred))

        # Save model and feature names
        joblib.dump(self.model, self.model_out_path)
        joblib.dump(X.columns.tolist(), self.features_out_path)
        print(f"[INFO] Saved model to: {self.model_out_path}")
        print(f"[INFO] Saved feature names to: {self.features_out_path}")

        return self.model, accuracy


if __name__ == "__main__":
    # Example usage - update the paths as necessary
    trainer = PhishingAwarenessModelTrainer(
        dataset_path='phishing_form.csv',
        answer_sheet_path='answer_sheetphi.json',
        model_out_path='phishing_awareness_model.pkl',
        features_out_path='phishing_feature_names.pkl'
    )

    model, accuracy = trainer.train_model()

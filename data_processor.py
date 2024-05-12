import pandas as pd
import re
from html import unescape

class AbstractProcessor:
    def __init__(self):
        self.default_patterns = [
            r'\$.*?\$',  # Inline math expressions enclosed in $
            r'\\[a-zA-Z]+\{.*?\}',  # LaTeX commands
            r'\w+_{[^}]+}',  # Subscripts
            r"(?<!\w)'(?!\w)",  # Primes that do not follow or precede word characters
            r'\w+_{[^}]+}\'?',  # Subscripts followed by an optional prime
            r'\w+^{-?\d+}',  # Superscripts
            r'\{[^}]+\}',  # Expressions enclosed in braces
            r'\[[^\]]+\]',  # Expressions enclosed in square brackets
            r'\^',  # Caret symbol
        ]

    def clean_text(self, text):
        # Unescape HTML entities and normalize text first
        text = unescape(text.replace('\n', ' '))

        # Specific substitution to handle escaped apostrophes and middle initials
        text = re.sub(r"\\'", '', text)  # Remove escaped apostrophes
        text = re.sub(r'\.-', '.', text)  # Correct middle initial formatting if necessary

        # Replace math expressions and LaTeX commands
        for pattern in self.default_patterns:
            text = re.sub(pattern, ' [MATH_EXPR] ', text)

        # Normalize whitespace after replacements
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def replace_math_expressions(self, text):
        replacement = ' [MATH_EXPR] '
        for pattern in self.default_patterns:
            text = re.sub(pattern, replacement, text)
        text = re.sub(r'(\s*\[MATH_EXPR\]\s*)+', ' [MATH_EXPR] ', text)
        return text

    def find_special_signs(self, col, patterns=None):
        if patterns is None:
            patterns = self.default_patterns
        special_signs = set()
        if isinstance(col, pd.Series):  # Check if the input is a Series
            for text in col:
                for pattern in patterns:
                    matches = re.findall(pattern, text)
                    special_signs.update(matches)
        else:
            for pattern in patterns:
                matches = re.findall(pattern, col)  # This assumes 'col' is a single string
                special_signs.update(matches)
        return special_signs


    def process(self, series, func=None):
        """
        Applies a specified function to each entry in a pandas Series.
        """
        if func:
            return series.apply(func)
        else:
            return series.apply(self.clean_text)

    def analyze_columns(self, dataframe, columns):
        special_signs_by_column = {}
        for column in columns:
            # Using 'process' to apply 'find_special_signs' across the column
            results = self.process(dataframe[column], lambda x: self.find_special_signs(x))
            # Aggregate results from each row
            column_signs = set()
            for result in results:
                column_signs.update(result)
            special_signs_by_column[column] = column_signs
        return special_signs_by_column

    def find_and_clean_special_signs(self, text):
        # Find signs without expecting the text back
        special_signs = self.find_special_signs(text)
        # Clean the text
        cleaned_text = self.clean_text(text)
        return cleaned_text


from sklearn.preprocessing import MultiLabelBinarizer

def multi_bin(df):
    # Flatten the list of lists in 'terms' column to get all labels in a single list
    all_labels = [label for sublist in df['terms'] for label in sublist]
    
    # # Count the frequency of each unique label and sort them by frequency in descending order
    # label_counts = Counter(all_labels)
    # sorted_label_counts = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)
    # print("Frequency of each label in 'terms' (sorted by frequency):")
    # for label, count in sorted_label_counts:
    #     print(f"{label}: {count}")
    
    # Extract unique labels (optional, as MultiLabelBinarizer does this internally)
    unique_labels = set(all_labels)
    print(f"\nUnique labels in 'terms': {unique_labels}")
    print(f"\nNumber of unique labels: {len(unique_labels)}")
    
    mlb = MultiLabelBinarizer()
    encoded_terms = mlb.fit_transform(df['terms'])
    terms_df = pd.DataFrame(encoded_terms, columns=mlb.classes_)
    
    df_ready_encoded = pd.concat([df.reset_index(drop=True), terms_df.reset_index(drop=True)], axis=1)
    
    print("\n", df_ready_encoded.head())
    print("Number of unique columns (including original ones):", df_ready_encoded.shape[1])

    return df_ready_encoded

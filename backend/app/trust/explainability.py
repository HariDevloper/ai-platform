import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance

class Explainability:
    def __init__(self, model):
        self.model = model

    def permutation_importance(self, X, y, n_repeats=30, random_state=None):
        result = permutation_importance(self.model, X, y, n_repeats=n_repeats, random_state=random_state)
        return result.importances_mean

    def feature_importance(self):
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        else:
            raise ValueError("Model does not have feature importances.")

    def get_top_features(self, X, n=10):
        importances = self.feature_importance()
        indices = np.argsort(importances)[-n:][::-1]
        return {f'Feature {i}': importances[i] for i in indices}

    def explain_prediction(self, X):
        # Explanation logic here, could utilize SHAP or LIME
        pass

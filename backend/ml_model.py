"""
ML Recommendation Model extracted from Jupyter Notebook
Content-based filtering using TF-IDF and Cosine Similarity
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class PGRecommender:
    """Smart PG Recommendation Engine"""
    
    def __init__(self, df=None):
        """
        Initialize the recommender with dataset
        
        Args:
            df: DataFrame with PG data
        """
        self.df = df
        self.similarity_matrix = None
        self.vectorizer = CountVectorizer()
        self.feature_matrix = None
        
        if df is not None and not df.empty:
            self._build_similarity_matrix()
    
    def _build_similarity_matrix(self):
        """Build cosine similarity matrix from PG features"""
        if self.df is None or self.df.empty:
            return
        
        # Create feature tags combining multiple attributes
        self.df['tags'] = (
            self.df['city'].astype(str) + " " +
            self.df['area_locality'].astype(str) + " " +
            self.df['furnishing_status'].astype(str) + " " +
            self.df['tenant_preferred'].astype(str)
        )
        
        # Transform text to feature matrix
        self.feature_matrix = self.vectorizer.fit_transform(self.df['tags'])
        
        # Calculate cosine similarity
        self.similarity_matrix = cosine_similarity(self.feature_matrix)
    
    def rent_category(self, price):
        """
        Categorize rent based on price
        
        Args:
            price: Rent amount in currency
            
        Returns:
            Category string
        """
        if price < 10000:
            return "low_rent"
        elif price < 20000:
            return "medium_rent"
        else:
            return "high_rent"
    
    def filter_pgs(self, city=None, max_budget=None, tenant_type=None, bhk=None):
        """
        Filter PGs based on user preferences
        
        Args:
            city: City name
            max_budget: Maximum rent budget
            tenant_type: Tenant type (Bachelors/Family)
            bhk: Number of BHKs
            
        Returns:
            DataFrame with filtered PGs
        """
        result = self.df.copy()
        
        if city:
            result = result[result['city'].str.contains(city, case=False, na=False)]
        
        if max_budget:
            result = result[result['rent'] <= max_budget]
        
        if tenant_type:
            result = result[result['tenant_preferred'].str.contains(tenant_type, case=False, na=False)]
        
        if bhk:
            result = result[result['bhk'] == bhk]
        
        return result
    
    def get_similar_pgs(self, locality, top_n=5):
        """
        Get similar PGs based on content similarity
        
        Args:
            locality: Area locality to find similar PGs for
            top_n: Number of recommendations
            
        Returns:
            DataFrame with similar PGs
        """
        if self.similarity_matrix is None:
            return pd.DataFrame()
        
        # Find index of the locality
        locality_indices = self.df[self.df['area_locality'] == locality].index.tolist()
        
        if not locality_indices:
            return pd.DataFrame()
        
        idx = locality_indices[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[idx].ravel()))
        
        # Sort by similarity score in descending order
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Skip the first one (itself) and get top N
        sim_scores = sim_scores[1:top_n+1]
        
        # Get indices of similar PGs
        similar_indices = [i[0] for i in sim_scores]
        
        return self.df.iloc[similar_indices].reset_index(drop=True)
    
    def recommend(self, city=None, max_budget=None, tenant_type=None, bhk=None, top_n=5):
        """
        Get PG recommendations based on user preferences
        
        Args:
            city: Preferred city
            max_budget: Maximum rent budget
            tenant_type: Tenant type preference
            bhk: Number of bedrooms
            top_n: Number of recommendations
            
        Returns:
            DataFrame with recommended PGs
        """
        # Filter based on preferences
        filtered = self.filter_pgs(city, max_budget, tenant_type, bhk)
        
        # If no results, return empty
        if filtered.empty:
            return pd.DataFrame()
        
        # Sort by price and rating
        filtered = filtered.sort_values(
            by=['rent', 'rating'],
            ascending=[True, False]
        )
        
        return filtered.head(top_n).reset_index(drop=True)


# Initialize global recommender
recommender = None

def initialize_recommender(csv_path):
    """Initialize the recommender with dataset"""
    global recommender
    
    try:
        df = pd.read_csv(csv_path)
        
        # Standardize column names to lowercase
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Select relevant columns
        required_cols = ['city', 'bhk', 'rent', 'area_locality', 
                        'furnishing_status', 'tenant_preferred', 'bathroom']
        
        # Keep only available columns
        available_cols = [col for col in required_cols if col in df.columns]
        df = df[available_cols]
        
        # Drop rows with missing values
        df = df.dropna().reset_index(drop=True)
        
        # Initialize recommender
        recommender = PGRecommender(df)
        return True
    except Exception as e:
        print(f"Error initializing recommender: {str(e)}")
        return False

def get_recommendations(city=None, max_budget=None, tenant_type=None, bhk=None, top_n=5):
    """
    Get PG recommendations
    
    Args:
        city: Preferred city
        max_budget: Maximum rent budget
        tenant_type: Tenant type preference
        bhk: Number of bedrooms
        top_n: Number of recommendations
        
    Returns:
        List of dictionaries with PG recommendations
    """
    global recommender
    
    if recommender is None:
        return []
    
    recommendations = recommender.recommend(city, max_budget, tenant_type, bhk, top_n)
    
    # Convert to list of dictionaries
    return recommendations.to_dict('records') if not recommendations.empty else []

def get_similar_recommendations(locality, top_n=5):
    """
    Get similar PGs to a specific locality
    
    Args:
        locality: Area locality
        top_n: Number of recommendations
        
    Returns:
        List of dictionaries with similar PGs
    """
    global recommender
    
    if recommender is None:
        return []
    
    similar = recommender.get_similar_pgs(locality, top_n)
    
    return similar.to_dict('records') if not similar.empty else []

"""Service for comparing text using ModernBert semantic similarity."""

import re
from typing import Optional, Tuple, Dict, Any
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class SimilarityComparator:
    """Service for comparing text similarity using ModernBert embeddings."""
    
    def __init__(self):
        """Initialize the similarity comparator with ModernBert model."""
        self.model_name = "answerdotai/ModernBERT-base"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load tokenizer and model
        print(f"Loading ModernBert model: {self.model_name} on {self.device}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()  # Set to evaluation mode
            print("ModernBert model loaded successfully!")
        except Exception as e:
            print(f"Warning: Could not load ModernBert model: {e}")
            print("Falling back to CPU-only mode or alternative model...")
            # Try without GPU
            self.device = "cpu"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for comparison.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def _get_embeddings(self, text: str) -> np.ndarray:
        """
        Get ModernBert embeddings for a text.
        
        Args:
            text: Text to encode
            
        Returns:
            Numpy array of embeddings (mean pooled)
        """
        # Tokenize and encode
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # Move inputs to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use mean pooling of all token embeddings (excluding padding)
            # Get attention mask to exclude padding tokens
            attention_mask = inputs['attention_mask']
            # Sum embeddings, excluding padding
            embeddings = outputs.last_hidden_state * attention_mask.unsqueeze(-1)
            # Sum and divide by number of non-padding tokens
            sum_embeddings = embeddings.sum(dim=1)
            sum_mask = attention_mask.sum(dim=1, keepdim=True)
            mean_pooled = sum_embeddings / sum_mask
        
        # Convert to numpy and return
        return mean_pooled.cpu().numpy()[0]
    
    def calculate_similarity(
        self,
        text1: str,
        text2: str
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate cosine similarity between two texts using ModernBert embeddings.
        
        Args:
            text1: First text to compare
            text2: Second text to compare
            
        Returns:
            Tuple of (similarity_score, metadata_dict)
            similarity_score: Float between 0 and 1 (1 = identical, 0 = completely different)
            metadata: Dictionary with additional comparison information
        """
        # Preprocess texts
        processed_text1 = self.preprocess_text(text1)
        processed_text2 = self.preprocess_text(text2)
        
        # Handle empty texts
        if not processed_text1 and not processed_text2:
            return 1.0, {"note": "Both texts are empty", "method": "modernbert"}
        
        if not processed_text1 or not processed_text2:
            return 0.0, {"note": "One text is empty", "method": "modernbert"}
        
        try:
            # Get embeddings for both texts
            embedding1 = self._get_embeddings(processed_text1)
            embedding2 = self._get_embeddings(processed_text2)
            
            # Reshape for cosine_similarity (needs 2D array)
            embedding1 = embedding1.reshape(1, -1)
            embedding2 = embedding2.reshape(1, -1)
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(embedding1, embedding2)
            similarity_score = float(similarity_matrix[0][0])
            
            # Ensure score is between 0 and 1 (cosine similarity can be -1 to 1)
            # For semantic similarity, we typically normalize to 0-1 range
            similarity_score = max(0.0, similarity_score)  # Clamp to 0-1
            
            # Calculate additional metrics
            text1_length = len(processed_text1.split())
            text2_length = len(processed_text2.split())
            length_ratio = min(text1_length, text2_length) / max(text1_length, text2_length) if max(text1_length, text2_length) > 0 else 0
            
            metadata = {
                "similarity_score": similarity_score,
                "text1_length": text1_length,
                "text2_length": text2_length,
                "length_ratio": length_ratio,
                "method": "modernbert_semantic_similarity",
                "model": self.model_name,
                "device": self.device
            }
            
            return similarity_score, metadata
            
        except Exception as e:
            # Fallback to simple word overlap if embedding fails
            return self._fallback_similarity(processed_text1, processed_text2, str(e))
    
    def _fallback_similarity(
        self,
        text1: str,
        text2: str,
        error_msg: str
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Fallback similarity calculation using simple word overlap.
        
        Args:
            text1: First text
            text2: Second text
            error_msg: Error message from main method
            
        Returns:
            Tuple of (similarity_score, metadata_dict)
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0, {"note": "Both texts are empty", "error": error_msg, "method": "jaccard_fallback"}
        
        if not words1 or not words2:
            return 0.0, {"note": "One text is empty", "error": error_msg, "method": "jaccard_fallback"}
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        jaccard_similarity = len(intersection) / len(union) if union else 0.0
        
        metadata = {
            "similarity_score": jaccard_similarity,
            "method": "jaccard_fallback",
            "error": error_msg,
            "common_words": len(intersection),
            "total_unique_words": len(union)
        }
        
        return jaccard_similarity, metadata
    
    def compare_with_threshold(
        self,
        text1: str,
        text2: str,
        threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Compare two texts and return detailed results with threshold check.
        
        Args:
            text1: First text (usually LLM response)
            text2: Second text (usually expected output)
            threshold: Similarity threshold for "match" (default: 0.7)
            
        Returns:
            Dictionary with comparison results
        """
        similarity_score, metadata = self.calculate_similarity(text1, text2)
        
        is_match = similarity_score >= threshold
        
        return {
            "similarity_score": similarity_score,
            "is_match": is_match,
            "threshold": threshold,
            "metadata": metadata,
            "text1_preview": text1[:100] + "..." if len(text1) > 100 else text1,
            "text2_preview": text2[:100] + "..." if len(text2) > 100 else text2,
        }


# Singleton instance
similarity_comparator = SimilarityComparator()

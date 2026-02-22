"""Service for comparing text using ModernBert semantic similarity."""

import re
from typing import Optional, Tuple, Dict, Any

# BERT and cosine similarity model loading disabled - only external LLM API calls used
# import torch
# from transformers import AutoTokenizer, AutoModel
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np


class SimilarityComparator:
    """Service for comparing text similarity using ModernBert embeddings (or Jaccard fallback)."""
    
    def __init__(self):
        """Initialize the similarity comparator. Model loading disabled - uses Jaccard fallback."""
        self.model_name = "answerdotai/ModernBERT-base"
        self.device = "cpu"
        self.tokenizer = None
        self.model = None
        
        # BERT/cosine similarity model loading commented out - only external LLM API calls are used
        # print(f"Loading ModernBert model: {self.model_name} on {self.device}...")
        # try:
        #     self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        #     self.model = AutoModel.from_pretrained(self.model_name)
        #     self.model.to(self.device)
        #     self.model.eval()  # Set to evaluation mode
        #     print("ModernBert model loaded successfully!")
        # except Exception as e:
        #     print(f"Warning: Could not load ModernBert model: {e}")
        #     print("Falling back to CPU-only mode or alternative model...")
        #     self.device = "cpu"
        #     self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        #     self.model = AutoModel.from_pretrained(self.model_name)
        #     self.model.to(self.device)
        #     self.model.eval()
    
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
    
    # BERT embeddings disabled - uncomment when re-enabling model
    # def _get_embeddings(self, text: str) -> np.ndarray:
    #     inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    #     inputs = {k: v.to(self.device) for k, v in inputs.items()}
    #     with torch.no_grad():
    #         outputs = self.model(**inputs)
    #         attention_mask = inputs['attention_mask']
    #         embeddings = outputs.last_hidden_state * attention_mask.unsqueeze(-1)
    #         sum_embeddings = embeddings.sum(dim=1)
    #         sum_mask = attention_mask.sum(dim=1, keepdim=True)
    #         mean_pooled = sum_embeddings / sum_mask
    #     return mean_pooled.cpu().numpy()[0]
    
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
            return 0.0, {"note": "One text is empty", "method": "jaccard_fallback"}
        
        # BERT/cosine similarity disabled - use Jaccard fallback only
        return self._fallback_similarity(
            processed_text1, processed_text2,
            "BERT/cosine similarity models disabled - using Jaccard fallback"
        )
    
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

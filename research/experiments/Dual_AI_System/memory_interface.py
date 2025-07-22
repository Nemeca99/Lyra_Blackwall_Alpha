#!/usr/bin/env python3
"""
Memory Interface for Dual AI System
Handles FAISS vector search and BGE embeddings
"""

import json
import logging
import os
import warnings
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime

# Set up logger first
logger = logging.getLogger(__name__)

# Import FAISS and BGE dependencies
try:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
    BGE_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    BGE_AVAILABLE = False
    logger.warning("FAISS or BGE not available - using fallback memory system")


class MemoryInterface:
    """Memory interface with FAISS vector search and BGE embeddings"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.embedding_model = config.get("embedding_model", "BAAI/bge-small-en-v1.5")
        self.vector_database = config.get("vector_database", "faiss")
        self.max_results = config.get("max_results", 10)
        self.similarity_threshold = config.get("similarity_threshold", 0.7)
        self.memory_path = config.get("memory_path", "memory")
        self.index_path = config.get("index_path", "memory/faiss_index")
        
        # Initialize components
        self.is_initialized = False
        self.embedding_model_loaded = False
        self.embedder = None
        self.index = None
        self.memory_metadata = []
        
        # Create directories
        Path(self.memory_path).mkdir(exist_ok=True)
        Path(self.index_path).mkdir(exist_ok=True)

    async def initialize(self):
        """Initialize FAISS index and BGE embeddings"""
        try:
            if not self.enabled:
                logger.info("Memory interface disabled")
                return

            logger.info("🔧 Initializing Memory Interface with FAISS + BGE")

            # Load BGE embedding model
            if BGE_AVAILABLE:
                try:
                    self.embedder = SentenceTransformer(self.embedding_model)
                    self.embedding_model_loaded = True
                    logger.info(f"✅ Loaded BGE model: {self.embedding_model}")
                except Exception as e:
                    logger.error(f"❌ Failed to load BGE model: {e}")
                    self.embedding_model_loaded = False

            # Initialize or load FAISS index
            if FAISS_AVAILABLE and self.embedding_model_loaded:
                try:
                    index_file = Path(self.index_path) / "memory_index.faiss"
                    metadata_file = Path(self.index_path) / "memory_metadata.json"
                    
                    if index_file.exists() and metadata_file.exists():
                        # Load existing index
                        self.index = faiss.read_index(str(index_file))
                        with open(metadata_file, 'r') as f:
                            self.memory_metadata = json.load(f)
                        logger.info(f"✅ Loaded existing FAISS index with {len(self.memory_metadata)} memories")
                    else:
                        # Create new index
                        dimension = self.embedder.get_sentence_embedding_dimension()
                        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
                        self.memory_metadata = []
                        logger.info(f"✅ Created new FAISS index with dimension {dimension}")
                    
                    self.is_initialized = True
                    logger.info("✅ Memory interface initialized successfully")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to initialize FAISS index: {e}")
                    self.is_initialized = False
            else:
                logger.warning("⚠️ FAISS or BGE not available - using fallback mode")
                self.is_initialized = True

        except Exception as e:
            logger.error(f"Failed to initialize Memory Interface: {e}")
            raise

    async def search_memory(self, query: str) -> List[Dict[str, Any]]:
        """
        Search memory for relevant context using FAISS + BGE or fallback text matching

        Args:
            query: Search query

        Returns:
            List of relevant memory items
        """
        try:
            if not self.enabled or not self.is_initialized:
                return []

            # Use FAISS + BGE if available
            if FAISS_AVAILABLE and self.embedding_model_loaded and self.index is not None:
                # Encode query
                query_embedding = self.embedder.encode([query], normalize_embeddings=True)
                
                # Search FAISS index
                scores, indices = self.index.search(query_embedding, min(self.max_results, len(self.memory_metadata)))
                
                # Filter by similarity threshold and return results
                results = []
                for score, idx in zip(scores[0], indices[0]):
                    if idx < len(self.memory_metadata) and score >= self.similarity_threshold:
                        memory_item = self.memory_metadata[idx].copy()
                        memory_item['similarity_score'] = float(score)
                        results.append(memory_item)

                logger.debug(f"FAISS search found {len(results)} relevant items for: {query[:50]}...")
                return results

            # Fallback: Simple text matching
            else:
                query_lower = query.lower()
                results = []
                
                for memory in self.memory_metadata:
                    content_lower = memory['content'].lower()
                    
                    # Simple keyword matching
                    query_words = query_lower.split()
                    content_words = content_lower.split()
                    
                    # Calculate simple similarity (word overlap)
                    common_words = set(query_words) & set(content_words)
                    if common_words:
                        similarity = len(common_words) / max(len(query_words), 1)
                        
                        if similarity >= self.similarity_threshold:
                            memory_item = memory.copy()
                            memory_item['similarity_score'] = similarity
                            results.append(memory_item)
                
                # Sort by similarity and limit results
                results.sort(key=lambda x: x['similarity_score'], reverse=True)
                logger.debug(f"Fallback search found {len(results)} relevant items for: {query[:50]}...")
                return results[:self.max_results]

        except Exception as e:
            logger.error(f"Error searching memory: {e}")
            return []

    async def store_memory(self, content: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Store new memory item using FAISS + BGE or fallback JSON storage

        Args:
            content: Memory content
            metadata: Additional metadata

        Returns:
            Success status
        """
        try:
            if not self.enabled or not self.is_initialized:
                return False

            # Prepare metadata
            memory_metadata = {
                'content': content,
                'timestamp': datetime.now().isoformat(),
                'id': len(self.memory_metadata),
                **(metadata or {})
            }

            # Use FAISS + BGE if available
            if FAISS_AVAILABLE and self.embedding_model_loaded and self.index is not None:
                # Encode content
                content_embedding = self.embedder.encode([content], normalize_embeddings=True)
                
                # Add to FAISS index
                self.index.add(content_embedding)
                self.memory_metadata.append(memory_metadata)

                # Save index and metadata
                await self._save_index()
                logger.debug(f"Stored memory with FAISS: {content[:50]}...")
                return True

            # Fallback: Simple JSON storage
            else:
                self.memory_metadata.append(memory_metadata)
                await self._save_fallback_memory()
                logger.debug(f"Stored memory with fallback: {content[:50]}...")
                return True

        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            return False

    async def _save_index(self):
        """Save FAISS index and metadata to disk"""
        try:
            if self.index is not None:
                index_file = Path(self.index_path) / "memory_index.faiss"
                metadata_file = Path(self.index_path) / "memory_metadata.json"
                
                faiss.write_index(self.index, str(index_file))
                with open(metadata_file, 'w') as f:
                    json.dump(self.memory_metadata, f, indent=2)
                
                logger.debug(f"Saved FAISS index with {len(self.memory_metadata)} memories")
        except Exception as e:
            logger.error(f"Error saving index: {e}")

    async def _save_fallback_memory(self):
        """Save fallback memory to JSON file"""
        try:
            metadata_file = Path(self.index_path) / "memory_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(self.memory_metadata, f, indent=2)
            
            logger.debug(f"Saved fallback memory with {len(self.memory_metadata)} memories")
        except Exception as e:
            logger.error(f"Error saving fallback memory: {e}")

    async def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        try:
            if not self.enabled:
                return {"enabled": False}

            stats = {
                "enabled": True,
                "initialized": self.is_initialized,
                "embedding_model": self.embedding_model,
                "vector_database": self.vector_database,
                "max_results": self.max_results,
                "similarity_threshold": self.similarity_threshold,
                "memory_path": self.memory_path,
                "index_path": self.index_path,
                "embedding_model_loaded": self.embedding_model_loaded,
                "faiss_available": FAISS_AVAILABLE,
                "bge_available": BGE_AVAILABLE,
            }

            if self.is_initialized and self.index is not None:
                stats.update({
                    "total_memories": len(self.memory_metadata),
                    "index_size": self.index.ntotal,
                    "index_dimension": self.index.d if hasattr(self.index, 'd') else None,
                })

            return stats

        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {"enabled": False, "error": str(e)}

    async def get_status(self) -> Dict[str, Any]:
        """Get current status of memory interface"""
        return {
            "enabled": self.enabled,
            "initialized": self.is_initialized,
            "embedding_model": self.embedding_model,
            "vector_database": self.vector_database,
            "faiss_available": FAISS_AVAILABLE,
            "bge_available": BGE_AVAILABLE,
            "embedding_model_loaded": self.embedding_model_loaded,
            "total_memories": len(self.memory_metadata) if self.memory_metadata else 0,
        }

    async def shutdown(self):
        """Shutdown memory interface"""
        try:
            if self.is_initialized:
                await self._save_index()
                logger.info("✅ Memory interface shutdown complete")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

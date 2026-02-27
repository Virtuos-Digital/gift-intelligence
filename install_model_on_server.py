#!/usr/bin/env python3
"""
One-time model installation script for server
Run this ONCE on the server to download and cache the model
"""
from sentence_transformers import SentenceTransformer
import os

# Model will be saved in a persistent location on server
MODEL_CACHE_DIR = "/opt/models/minilm"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("="*80)
print("Installing MiniLM Model on Server")
print("="*80)
print(f"\nModel: {MODEL_NAME}")
print(f"Installation directory: {MODEL_CACHE_DIR}")
print("\nThis is a ONE-TIME setup. The model will be cached permanently.\n")

# Create directory if it doesn't exist
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)

# Download and save model
print("Downloading model from HuggingFace...")
model = SentenceTransformer(MODEL_NAME)
model.save(MODEL_CACHE_DIR)

print("\n✅ Model installed successfully!")
print(f"   Location: {MODEL_CACHE_DIR}")
print(f"   Size: ~90MB")
print("\nYou can now deploy your app without model files.")
print("="*80)

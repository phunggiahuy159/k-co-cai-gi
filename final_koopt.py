#!pip install datasets pyvi transformers 
from pyvi import ViTokenizer
from transformers import AutoTokenizer
from datasets import load_dataset
from torch.utils.data import DataLoader
from tqdm import tqdm
import torch
import numpy as np

def segment_text(text):
    return ViTokenizer.tokenize(text)from datasets import load_dataset
# Load the UIT-ViQuAD2.0 dataset
dataset = load_dataset("taidng/UIT-ViQuAD2.0")

# Load the BKAi tokenizer
from transformers import RobertaTokenizerFast
tokenizer = RobertaTokenizerFast.from_pretrained('vinai/phobert-base')

# Segmentation + Tokenization
def preprocess_function(examples):
    # Segment questions and contexts
    segmented_questions = [ViTokenizer.tokenize(q) for q in examples["question"]]
    segmented_contexts = [ViTokenizer.tokenize(c) for c in examples["context"]]
    
    # Tokenize segmented text
    tokenized = tokenizer(segmented_questions, segmented_contexts, truncation=True, padding=True, max_length=512, return_offsets_mapping=True
)
    return tokenized

# Apply preprocessing
encoded_dataset = dataset.map(preprocess_function, batched=True)

# Convert the dataset to PyTorch tensors
encoded_dataset.set_format(type="torch", columns=['id', 'uit_id', 'title', 'context', 'question', 'answers', 'is_impossible', 'plausible_answers', 'input_ids', 'attention_mask', 'offset_mapping'])

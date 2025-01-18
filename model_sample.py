from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline
import tensorflow as tf

# Load the model and tokenizer
model_name = "phi-4"  
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)



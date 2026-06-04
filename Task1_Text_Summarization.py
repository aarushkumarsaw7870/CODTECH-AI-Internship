from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

print("Model aur Tokenizer load ho rahe hain... Thoda wait karein...")

# Model ka naam
model_name = "facebook/bart-large-cnn"

# Model aur Tokenizer ko direct load karna
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print("\n--- Text Summarization Tool ---")
print("Apna lengthy article yahan paste karein.")
print("Paste karne ke baad naye line me jaakar 'DONE' likhein aur Enter dabayein:\n")

# Multiple lines input lene ke liye loop
lines = []
while True:
    line = input()
    if line.strip() == "DONE":
        break
    lines.append(line)

text = "\n".join(lines)

if text.strip() == "":
    print("Error: Aapne koi text enter nahi kiya!")
else:
    print("\nSummary generate ho rahi hai... Thoda intezar karein...")
    
    # Text ko AI ke samajhne layak tokens mein badalna
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    
    # Summary generate karna
    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=40, length_penalty=2.0)
    
    # Tokens ko wapas text mein badalna
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    print("\n" + "="*40)
    print("--- Summarized Text ---")
    print("="*40)
    print(summary)
    print("="*40)
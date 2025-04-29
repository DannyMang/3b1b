import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
import wandb
from config import Config

def main():
    # Initialize wandb
    wandb.init(project="3b1b-model", config=vars(Config))
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(Config.MODEL_NAME)
    
    # Load and prepare dataset
    def tokenize_function(examples):
        return tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=Config.MAX_LENGTH
        )
    
    # Load your dataset here
    # For now, we'll use a placeholder
    dataset = load_dataset("json", data_files={
        "train": Config.TRAIN_FILE,
        "validation": Config.VALIDATION_FILE
    })
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=Config.OUTPUT_DIR,
        num_train_epochs=Config.NUM_EPOCHS,
        per_device_train_batch_size=Config.BATCH_SIZE,
        per_device_eval_batch_size=Config.BATCH_SIZE,
        warmup_steps=Config.WARMUP_STEPS,
        weight_decay=Config.WEIGHT_DECAY,
        logging_dir=Config.LOGGING_DIR,
        logging_steps=Config.LOGGING_STEPS,
        save_steps=Config.SAVE_STEPS,
        evaluation_strategy="steps",
        load_best_model_at_end=True,
        report_to="wandb"
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    )
    
    # Train the model
    trainer.train()
    
    # Save the final model
    trainer.save_model(Config.OUTPUT_DIR)
    tokenizer.save_pretrained(Config.OUTPUT_DIR)

if __name__ == "__main__":
    main() 
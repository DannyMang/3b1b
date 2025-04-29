class Config:
    # Model parameters
    MODEL_NAME = "facebook/opt-125m"  # Starting with a small model
    MAX_LENGTH = 512
    BATCH_SIZE = 8
    LEARNING_RATE = 2e-5
    NUM_EPOCHS = 3
    WARMUP_STEPS = 100
    
    # Training parameters
    GRADIENT_ACCUMULATION_STEPS = 4
    WEIGHT_DECAY = 0.01
    LOGGING_STEPS = 100
    SAVE_STEPS = 1000
    
    # Data parameters
    TRAIN_FILE = "data/train.jsonl"
    VALIDATION_FILE = "data/validation.jsonl"
    TEST_FILE = "data/test.jsonl"
    
    # Output parameters
    OUTPUT_DIR = "output"
    LOGGING_DIR = "logs" 
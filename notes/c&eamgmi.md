#Characterizing and Efficiently Accelerating Multimodal Generation Model Inference

 1) llama for code generation, code llama is trained on wide range of input seq lengths to handle varying sizes of code snippets
 2) Embedding layer => transformer decoder block ( attention + feed forward layer), 34B model / 48 layers transformer decoder blocka
 3) Auto regressive nature of token generation (llama, etc) makes decoding a performance - critical phase that is primarily determined by # decoding steps, the number of decoding steps matters the most to the end-to-end latency
 4) inference time of autoregressive models is often dominated by GPU idle time, => implies models are heavily dependent on CPU-bound modules
 5) linear opeations make up a big portion of the overall model inference latency. attention opertions in the FFN in transformer-based models is dominates the e2e inference time 

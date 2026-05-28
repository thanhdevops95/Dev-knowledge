# Deep Learning — Neural Networks, CNNs, Transformers

> **Tags:** `deep-learning` `neural-networks` `cnn` `transformer` `pytorch` `nlp` `computer-vision`
> **Level:** Advanced | **Prerequisite:** `ai-ml/03-ml-supervised-unsupervised.md`

---

## 1. Neural Network Fundamentals

```
Neuron:
  input * weight + bias → activation function → output
  
  z = Σ(w_i * x_i) + b
  a = f(z)    # f = activation function (ReLU, Sigmoid, Tanh, etc.)

Fully Connected (Dense) Layer:
  z = W * x + b     # Matrix multiplication
  a = f(z)

Layer 1: input  → 784 neurons  (28x28 image pixels)
Layer 2: hidden → 256 neurons  (representations)
Layer 3: hidden → 128 neurons  (higher-level features)
Layer 4: output → 10 neurons   (class probabilities)
```

```python
import torch
import torch.nn as nn
import torch.optim as optim

# Define neural network
class MLP(nn.Module):
    def __init__(self, input_size: int, hidden_sizes: list[int], output_size: int, dropout: float = 0.3):
        super().__init__()
        
        layers = []
        in_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(in_size, hidden_size),
                nn.BatchNorm1d(hidden_size),
                nn.ReLU(),
                nn.Dropout(dropout),
            ])
            in_size = hidden_size
        
        layers.append(nn.Linear(in_size, output_size))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

model = MLP(input_size=784, hidden_sizes=[512, 256, 128], output_size=10)
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
```

---

## 2. Training Loop

```python
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for batch_idx, (data, targets) in enumerate(tqdm(loader)):
        data, targets = data.to(device), targets.to(device)
        
        # Forward pass
        outputs = model(data)
        loss = criterion(outputs, targets)
        
        # Backward pass
        optimizer.zero_grad()   # Clear gradients
        loss.backward()         # Compute gradients
        
        # Gradient clipping (prevent exploding gradients)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()        # Update weights
        
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)
    
    return total_loss / len(loader), correct / total

@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    for data, targets in loader:
        data, targets = data.to(device), targets.to(device)
        outputs = model(data)
        loss = criterion(outputs, targets)
        
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)
    
    return total_loss / len(loader), correct / total

# Training orchestration
device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
model = model.to(device)

optimizer = optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-2)
criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

scheduler = optim.lr_scheduler.OneCycleLR(
    optimizer, max_lr=1e-3,
    epochs=50, steps_per_epoch=len(train_loader)
)

best_val_acc = 0
patience = 10
patience_counter = 0

for epoch in range(50):
    train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device)
    val_loss, val_acc = evaluate(model, val_loader, criterion, device)
    scheduler.step()
    
    print(f"Epoch {epoch+1}: train_loss={train_loss:.4f} train_acc={train_acc:.4f} "
          f"val_loss={val_loss:.4f} val_acc={val_acc:.4f}")
    
    # Early stopping + checkpoint
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save({'epoch': epoch, 'model': model.state_dict(), 
                    'optimizer': optimizer.state_dict()}, 'best_model.pt')
        patience_counter = 0
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Early stopping at epoch {epoch+1}")
            break
```

---

## 3. CNNs — Computer Vision

```python
class ConvBlock(nn.Module):
    """Conv → BN → ReLU → (optional Pool)"""
    def __init__(self, in_channels: int, out_channels: int, pool: bool = False):
        super().__init__()
        layers = [
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        ]
        if pool:
            layers.append(nn.MaxPool2d(2))   # Halve spatial dims
        self.block = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.block(x)

class CNN(nn.Module):
    """Simple CNN for image classification"""
    def __init__(self, num_classes: int = 10):
        super().__init__()
        
        # Feature extractor (output: [B, 512, 4, 4] for 32x32 input)
        self.features = nn.Sequential(
            ConvBlock(3, 64),           # [B, 64, 32, 32]
            ConvBlock(64, 128, pool=True),  # [B, 128, 16, 16]
            ConvBlock(128, 256),        # [B, 256, 16, 16]
            ConvBlock(256, 512, pool=True), # [B, 512, 8, 8]
            ConvBlock(512, 512, pool=True), # [B, 512, 4, 4]
        )
        
        # Global Average Pooling (eliminates spatial dims)
        self.gap = nn.AdaptiveAvgPool2d((1, 1))
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.gap(x)
        return self.classifier(x)

# Transfer Learning — pretrained ResNet
import torchvision.models as models

class TransferModel(nn.Module):
    def __init__(self, num_classes: int, freeze_backbone: bool = True):
        super().__init__()
        
        # Load pretrained backbone
        self.backbone = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        
        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False   # Freeze all layers
        
        # Replace final classification head
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes),
        )
    
    def forward(self, x):
        return self.backbone(x)

# Fine-tuning: gradually unfreeze layers
model = TransferModel(num_classes=5, freeze_backbone=True)

# Phase 1: Only train head (high LR)
optimizer = optim.AdamW(model.backbone.fc.parameters(), lr=1e-3)
# ... 5 epochs

# Phase 2: Unfreeze last layers
for param in model.backbone.layer4.parameters():
    param.requires_grad = True

optimizer = optim.AdamW([
    {'params': model.backbone.layer4.parameters(), 'lr': 1e-5},
    {'params': model.backbone.fc.parameters(), 'lr': 1e-3},
])
```

---

## 4. Data Augmentation

```python
from torchvision import transforms
from torchvision.transforms import v2 as T

# Training augmentations
train_transform = T.Compose([
    T.RandomResizedCrop(224, scale=(0.7, 1.0)),
    T.RandomHorizontalFlip(p=0.5),
    T.RandomVerticalFlip(p=0.2),
    T.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
    T.RandomGrayscale(p=0.1),
    T.GaussianBlur(kernel_size=3, sigma=(0.1, 2.0)),
    T.ToImage(),
    T.ToDtype(torch.float32, scale=True),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Validation (no augmentation)
val_transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ToImage(),
    T.ToDtype(torch.float32, scale=True),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Mix-up augmentation (soft labels)
def mixup(inputs, labels, alpha=0.2):
    lam = np.random.beta(alpha, alpha)
    batch_size = inputs.size(0)
    index = torch.randperm(batch_size).to(inputs.device)
    
    mixed_inputs = lam * inputs + (1 - lam) * inputs[index]
    labels_a, labels_b = labels, labels[index]
    
    return mixed_inputs, labels_a, labels_b, lam

def mixup_criterion(criterion, pred, y_a, y_b, lam):
    return lam * criterion(pred, y_a) + (1 - lam) * criterion(pred, y_b)
```

---

## 5. Transformers & Self-Attention

```python
class SelfAttention(nn.Module):
    """Multi-Head Self-Attention"""
    
    def __init__(self, embed_dim: int, num_heads: int, dropout: float = 0.1):
        super().__init__()
        assert embed_dim % num_heads == 0
        
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.scale = self.head_dim ** -0.5
        
        self.qkv = nn.Linear(embed_dim, 3 * embed_dim, bias=False)
        self.out = nn.Linear(embed_dim, embed_dim)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        B, T, C = x.shape   # batch, sequence length, channels
        
        # Compute Q, K, V
        qkv = self.qkv(x).reshape(B, T, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)  # [3, B, heads, T, head_dim]
        q, k, v = qkv.unbind(0)
        
        # Scaled dot-product attention
        attn = (q @ k.transpose(-2, -1)) * self.scale   # [B, heads, T, T]
        
        if mask is not None:
            attn = attn.masked_fill(mask == 0, float('-inf'))
        
        attn = torch.softmax(attn, dim=-1)
        attn = self.dropout(attn)
        
        # Combine
        out = (attn @ v).transpose(1, 2).reshape(B, T, C)
        return self.out(out)

class TransformerBlock(nn.Module):
    def __init__(self, embed_dim: int, num_heads: int, ff_dim: int, dropout: float = 0.1):
        super().__init__()
        self.attention = SelfAttention(embed_dim, num_heads, dropout)
        self.ff = nn.Sequential(
            nn.Linear(embed_dim, ff_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(ff_dim, embed_dim),
        )
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
        # Pre-norm (more stable than post-norm)
        x = x + self.dropout(self.attention(self.norm1(x), mask))
        x = x + self.dropout(self.ff(self.norm2(x)))
        return x

class GPTModel(nn.Module):
    """Simple GPT-style language model"""
    
    def __init__(self, vocab_size: int, embed_dim: int, num_heads: int, 
                 num_layers: int, max_seq_len: int, dropout: float = 0.1):
        super().__init__()
        
        self.token_emb = nn.Embedding(vocab_size, embed_dim)
        self.pos_emb = nn.Embedding(max_seq_len, embed_dim)
        self.dropout = nn.Dropout(dropout)
        
        self.blocks = nn.ModuleList([
            TransformerBlock(embed_dim, num_heads, embed_dim * 4, dropout)
            for _ in range(num_layers)
        ])
        
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, vocab_size, bias=False)
        
        # Weight tying (embedding + output head share weights)
        self.head.weight = self.token_emb.weight
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T = x.shape
        
        # Embeddings
        tok = self.token_emb(x)                                    # [B, T, C]
        pos = self.pos_emb(torch.arange(T, device=x.device))      # [T, C]
        x = self.dropout(tok + pos)
        
        # Causal mask (can't see future tokens)
        mask = torch.tril(torch.ones(T, T, device=x.device)).bool()
        
        for block in self.blocks:
            x = block(x, mask)
        
        x = self.norm(x)
        return self.head(x)   # [B, T, vocab_size]
    
    @torch.no_grad()
    def generate(self, prompt: torch.Tensor, max_new_tokens: int = 100, temperature: float = 0.8, top_k: int = 40):
        for _ in range(max_new_tokens):
            logits = self(prompt[:, -512:])[:, -1, :]   # Last token logits
            
            # Temperature scaling
            logits = logits / temperature
            
            # Top-k sampling
            if top_k > 0:
                values, _ = torch.topk(logits, top_k)
                logits[logits < values[:, -1:]] = float('-inf')
            
            probs = torch.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, 1)
            prompt = torch.cat([prompt, next_token], dim=-1)
        
        return prompt
```

---

## 6. Hugging Face — Using Pretrained Models

```python
from transformers import (
    AutoTokenizer, AutoModel, AutoModelForSequenceClassification,
    Trainer, TrainingArguments
)
from datasets import Dataset

# Text classification (sentiment)
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Tokenize
def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )

# HuggingFace Trainer
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    learning_rate=2e-5,
    weight_decay=0.01,
    warmup_ratio=0.1,
    fp16=True,        # Mixed precision
    logging_steps=50,
    report_to="wandb",  # Weights & Biases logging
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()

# Embeddings for semantic search
encoder = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def get_embeddings(texts: list[str]) -> np.ndarray:
    encoded = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        output = encoder(**encoded)
    
    # Mean pooling (attention_mask to ignore padding)
    embeddings = mean_pooling(output.last_hidden_state, encoded['attention_mask'])
    return nn.functional.normalize(embeddings, dim=1).numpy()

# Semantic similarity
def find_similar(query: str, corpus: list[str], top_k: int = 5):
    query_emb = get_embeddings([query])
    corpus_emb = get_embeddings(corpus)
    
    similarities = np.dot(query_emb, corpus_emb.T)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    return [(corpus[i], similarities[i]) for i in top_indices]
```

---

## 7. Common Architectures

```
Image Classification:
  AlexNet (2012) → VGG (2014) → ResNet (2015) → EfficientNet (2019)
  Key innovation: ResNet = residual connections (skip connections)
  
Object Detection:
  YOLO (v1-v10) — real-time, single pass
  Faster R-CNN — two-stage, more accurate
  DETR — transformer-based, end-to-end
  
Text:
  LSTM/GRU (2015) → Transformer (2017) → BERT (2018) → GPT-2/3/4
  BERT = bidirectional (understanding)
  GPT = autoregressive (generation)
  
Vision-Language:
  CLIP (2021) — image + text in same embedding space
  DALL-E, Stable Diffusion — text → image generation
  LLaVA — multimodal LLM
```

---

## 8. Optimization Techniques

```python
# Mixed Precision Training (2x faster, 2x memory savings)
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for data, targets in loader:
    optimizer.zero_grad()
    
    with autocast():   # FP16 forward pass
        outputs = model(data)
        loss = criterion(outputs, targets)
    
    scaler.scale(loss).backward()       # Scale loss → FP32 gradients
    scaler.step(optimizer)              # Unscale, update weights
    scaler.update()

# Gradient Accumulation (simulate larger batch)
accumulation_steps = 4

for i, (data, targets) in enumerate(loader):
    outputs = model(data)
    loss = criterion(outputs, targets) / accumulation_steps   # Normalize!
    loss.backward()
    
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()

# 8-bit Quantization (bitsandbytes)
import bitsandbytes as bnb

optimizer = bnb.optim.AdamW8bit(model.parameters(), lr=1e-4)

# LoRA — Parameter-Efficient Fine-tuning
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=8,                # Rank
    lora_alpha=32,      # Scaling factor
    target_modules=["q_proj", "v_proj"],  # Which layers to adapt
    lora_dropout=0.1,
    bias="none",
)

model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()  # Only 0.1% of params!
# → trainable params: 4,718,592 || all params: 7,241,732,096 || trainable%: 0.065%
```

---

*Tài liệu liên quan: `ai-ml/03-ml-supervised-unsupervised.md` | `python/02-python-advanced.md` | `ai-ml/05-llm-prompting.md`*

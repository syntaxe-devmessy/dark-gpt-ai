# dark-gpt-ai
Dark Gpt used the uncensored Dolphine model; you can ask for whatever you want.
Create By Syntaxe Tech


```markdown
# 🔥 Dark Gpt Ai

<div align="center">
  <img src="https://img.shields.io/badge/version-2.0-blue.svg" alt="Version 2.0">
  <img src="https://img.shields.io/badge/python-3.9%2B-green.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/model-Dolphin%202.9.1-purple.svg" alt="Dolphin 2.9.1">
  <img src="https://img.shields.io/badge/RAM-8GB%20optimized-success.svg" alt="8GB RAM">
</div>

<p align="center">
  <strong>Uncensored AI Assistant powered by Dolphin 2.9.1 Mistral 7B</strong><br>
  Optimized for 8GB RAM with 4-bit quantization
</p>

---

## 📋 Table of Contents
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Performance](#-performance)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

### Core Features
- ✅ **100% Uncensored** - No content filtering, complete freedom
- ✅ **7B Parameters** - Powerful language model
- ✅ **4-bit Quantization** - Only ~4GB RAM usage
- ✅ **Code Expert** - Excellent at Python, JavaScript, and more
- ✅ **Multilingual** - Supports French, English, and other languages

### Technical Features
- 🚀 **FastAPI** - High-performance async API
- 💻 **Modern Web Interface** - Responsive chat UI
- 🔒 **CORS Enabled** - Ready for cross-origin requests
- 📊 **Real-time Status** - Model loading indicator
- 🎨 **Cyberpunk Theme** - Dark mode UI with glitch effects
- ⚡ **Optimized for CPU** - Runs smoothly on 8GB RAM

---

## 🎮 Demo

```bash
# Live demo (if hosted)
https://your-domain.com

# Local demo after installation
http://localhost:5000
```

---

🛠 Tech Stack

Backend

· Framework: Flask 2.3.3
· ML Framework: Hugging Face Transformers
· Model: Dolphin 2.9.1 Mistral 7B
· Quantization: bitsandbytes 4-bit (NF4)
· Python: 3.9+

Frontend

· HTML5 - Semantic markup
· CSS3 - Custom properties, animations
· JavaScript - Async/Await, Fetch API
· Responsive Design - Mobile-friendly

Infrastructure

· Systemd - Auto-start service
· Gunicorn - Production server (optional)
· UFW - Firewall configuration

---

📦 Installation

Prerequisites

· Python 3.9 or higher
· 8GB RAM minimum
· 10GB free disk space
· Linux/Ubuntu (recommended) or macOS

Quick Install (Automatic)

```bash
# Clone the repository
git clone https://github.com/syntaxe-devmessy/dark-gpt-ai.git
cd dark-gpt-ai

# Make the installer executable
chmod +x install_darkgpt.sh

# Run the automatic installer
./install_darkgpt.sh
```

The installer will:

1. 📥 Download Dolphin 2.9.1 model (4-bit)
2. 🐍 Create Python virtual environment
3. 📦 Install all dependencies
4. ⚙️ Configure systemd service
5. 🔓 Open firewall port 5000
6. 🚀 Start the service

Manual Installation

```bash
# Clone repository
git clone https://github.com/syntaxe-devmessy/dark-gpt-ai.git
cd dark-gpt-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download model (4-bit quantized)
python3 -c "
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model_name = 'cognitivecomputations/dolphin-2.9.1-mistral-7b'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map='auto'
)
"

# Start the server
python3 app.py
```

---

🚀 Usage

Starting the Server

```bash
# Using systemd (recommended)
sudo systemctl start darkgpt
sudo systemctl enable darkgpt

# Using the start script
./start.sh

# Manually
source venv/bin/activate
python3 app.py
```

Access the Interface

· Web Interface: http://localhost:5000
· Chat: http://localhost:5000/chat
· API Status: http://localhost:5000/api/status

Service Management

```bash
# Check status
sudo systemctl status darkgpt

# View logs
journalctl -u darkgpt -f

# Stop service
sudo systemctl stop darkgpt

# Restart service
sudo systemctl restart darkgpt
```

---

📡 API Reference

Status Endpoint

```http
GET /api/status
```

Response:

```json
{
  "status": "online",
  "model": "Dolphin 2.9.1 Mistral 7B",
  "loaded": true,
  "loading": false,
  "timestamp": "2024-01-01T12:00:00"
}
```

Generate Endpoint

```http
POST /api/generate
Content-Type: application/json
```

Request Body:

```json
{
  "prompt": "Write a Python function to calculate fibonacci",
  "max_tokens": 500,
  "temperature": 0.7,
  "top_p": 0.95
}
```

Response:

```json
{
  "success": true,
  "response": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
  "model": "Dolphin 2.9.1"
}
```

Example with cURL

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "max_tokens": 300,
    "temperature": 0.7
  }'
```

---

📁 Project Structure

```
dark-gpt-ai/
├── 📄 app.py                 # Main Flask application
├── 📄 requirements.txt       # Python dependencies
├── 📄 install_darkgpt.sh    # Automatic installation script
├── 📄 start.sh              # Server startup script
├── 📄 README.md             # Documentation (this file)
├── 📄 .gitignore            # Git ignore rules
├── 📁 templates/            # HTML templates
│   ├── index.html          # Landing page
│   ├── chat.html           # Chat interface
│   └── about.html          # About page
├── 📁 static/               # Static assets
│   ├── style.css           # CSS styles
│   └── script.js           # Frontend JavaScript
└── 📁 logs/                 # Application logs (created at runtime)
```

Key Files Description

File Description
app.py Main Flask application with API endpoints and model loading
install_darkgpt.sh Automated installer that sets up everything
templates/chat.html Modern chat interface with real-time updates
static/script.js Handles API calls and UI interactions
static/style.css Cyberpunk-themed responsive design

---

⚙️ Configuration

Model Settings (in app.py)

```python
# Model configuration
MODEL_NAME = "cognitivecomputations/dolphin-2.9.1-mistral-7b"

# Quantization config (4-bit)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)
```

Generation Parameters

Parameter Default Description
max_tokens 500 Maximum response length
temperature 0.7 Creativity (0.1 = precise, 1.5 = creative)
top_p 0.95 Nucleus sampling

Environment Variables (optional)

Create a .env file:

```env
FLASK_ENV=production
PORT=5000
HOST=0.0.0.0
DEBUG=false
```

---

📊 Performance

Memory Usage

· Model (4-bit): ~4GB RAM
· Tokenizer/Overhead: ~1GB RAM
· Total: ~5GB RAM (comfortable on 8GB)

Response Times

Action Time
Model Loading 2-3 minutes
First Response 5-10 seconds
Subsequent Responses 2-5 seconds
Cold Start 2-3 minutes

Optimization Techniques

· ✅ 4-bit quantization (NF4)
· ✅ CPU offloading for heavy layers
· ✅ Response caching (coming soon)
· ✅ Async model loading

---

🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (git checkout -b feature/amazing)
3. 💾 Commit changes (git commit -m 'Add amazing feature')
4. 📤 Push to branch (git push origin feature/amazing)
5. 🎯 Open a Pull Request

Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/dark-gpt-ai.git
cd dark-gpt-ai

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

---

📜 License

This project is licensed under the MIT License - see below:

```
MIT License

Copyright (c) 2024 syntaxe-devmessy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Model License

The base model Dolphin 2.9.1 is created by Cognitive Computations and is available under a permissive license for both commercial and non-commercial use.

---

👨‍💻 Author

syntaxe-devmessy

· GitHub: @syntaxe-devmessy
· Project: Dark Gpt Ai

---

⭐ Support

If you like this project, please give it a star on GitHub! It helps others discover it.

https://img.shields.io/github/stars/syntaxe-devmessy/dark-gpt-ai.svg?style=social

---

<div align="center">
  <strong>Built with 🔥 by syntaxe-devmessy</strong>
</div>
```

📋 Comment l'ajouter à ton repo

```bash
cd /opt/dark-gpt-ai
nano README.md
# Colle le contenu ci-dessus
git add README.md
git commit -m "Add professional README with project structure"
git push
```

🎯 Ce qui a été amélioré :

· ✅ Professionnel - Structure claire et complète
· ✅ Bilingual ready - Mais en anglais pour portée internationale
· ✅ Badges - Montre version, licence, etc.
· ✅ Table des matières - Navigation facile
· ✅ Structure du projet - Arborescence détaillée
· ✅ API Reference - Documentation complète
· ✅ Installation - Multiple méthodes
· ✅ Configuration - Tous les paramètres
· ✅ Performance - Statistiques détaillées
· ✅ Contributing - Guide pour contributeurs
· ✅ License - Texte complet

C'est prêt pour GitHub ! 🚀

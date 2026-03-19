#!/bin/bash

# === Dark Gpt Ai - Script d'installation automatique ===
# Repo: https://github.com/syntaxe-devmessy/dark-gpt-ai
# Version: 2.0

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
REPO_URL="https://github.com/syntaxe-devmessy/dark-gpt-ai.git"
APP_DIR="$HOME/dark-gpt-ai"
PORT=5001

# Bannière
clear
echo -e "${PURPLE}"
echo '╔══════════════════════════════════════════════════════════╗'
echo '║         DARK GPT AI - INSTALLATEUR AUTOMATIQUE          ║'
echo '║                    Version 2.0 - 8GB RAM                ║'
echo '╚══════════════════════════════════════════════════════════╝'
echo -e "${NC}"
echo ""

# Vérification
echo -e "${BLUE}[1/8]${NC} Vérification du système..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 non trouvé. Installation...${NC}"
    sudo apt update && sudo apt install -y python3 python3-pip
fi

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git non trouvé. Installation...${NC}"
    sudo apt install -y git
fi

echo -e "${GREEN}✅ OK${NC}"

# Clone
echo -e "${BLUE}[2/8]${NC} Téléchargement de Dark Gpt Ai..."
if [ -d "$APP_DIR" ]; then
    echo -e "${YELLOW}📁 Dossier existant, mise à jour...${NC}"
    cd $APP_DIR && git pull
else
    git clone $REPO_URL $APP_DIR
fi

cd $APP_DIR
echo -e "${GREEN}✅ OK${NC}"

# Environnement virtuel
echo -e "${BLUE}[3/8]${NC} Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate
echo -e "${GREEN}✅ OK${NC}"

# Dépendances
echo -e "${BLUE}[4/8]${NC} Installation des dépendances Python..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✅ OK${NC}"

# Modèle
echo -e "${BLUE}[5/8]${NC} Téléchargement de Dolphin 2.9.1 (4-bit)..."
python3 -c "
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

print('📥 Téléchargement en cours...')
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model_name = 'cognitivecomputations/dolphin-2.9.1-mistral-7b'
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map='auto',
    torch_dtype=torch.float16,
    trust_remote_code=True
)
print('✅ Modèle prêt !')
" > /dev/null 2>&1
echo -e "${GREEN}✅ OK${NC}"

# Service systemd
echo -e "${BLUE}[6/8]${NC} Configuration du service..."

sudo bash -c "cat > /etc/systemd/system/darkgpt.service << EOF
[Unit]
Description=Dark Gpt Ai Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=\"PATH=$APP_DIR/venv/bin\"
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable darkgpt > /dev/null 2>&1
echo -e "${GREEN}✅ OK${NC}"

# Firewall
echo -e "${BLUE}[7/8]${NC} Configuration du firewall..."
if command -v ufw &> /dev/null; then
    sudo ufw allow $PORT/tcp > /dev/null 2>&1
    echo -e "${GREEN}✅ Port $PORT ouvert${NC}"
else
    echo -e "${YELLOW}⚠️  UFW non installé${NC}"
fi

# Démarrage
echo -e "${BLUE}[8/8]${NC} Démarrage de Dark Gpt Ai..."
sudo systemctl start darkgpt

# IP
IP=$(curl -s ifconfig.me 2>/dev/null || echo "localhost")

# Final
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ INSTALLATION TERMINÉE AVEC SUCCÈS !${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}🌐 Accès:${NC}"
echo -e "   Local:  ${YELLOW}http://localhost:$PORT${NC}"
echo -e "   Public: ${YELLOW}http://$IP:$PORT${NC}"
echo ""
echo -e "${CYAN}📋 Commandes:${NC}"
echo -e "   Démarrer:   ${YELLOW}sudo systemctl start darkgpt${NC}"
echo -e "   Arrêter:    ${YELLOW}sudo systemctl stop darkgpt${NC}"
echo -e "   Logs:       ${YELLOW}journalctl -u darkgpt -f${NC}"
echo -e "   Status:     ${YELLOW}systemctl status darkgpt${NC}"
echo ""
echo -e "${CYAN}📁 Dossier:${NC} ${YELLOW}$APP_DIR${NC}"
echo ""
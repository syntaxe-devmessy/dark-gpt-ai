# dark-gpt-ai
Dark Gpt used the uncensored Dolphine model; you can ask for whatever you want.
Create By Syntaxe Tech

# 🕸️ Dark Gpt Ai💀

**Uncensored AI Assistant** - Dolphin 2.9.1 Mistral 7B (4-bit)  
Created by **Syntaxe Tech**

---

## 📦 Installation sur VPS

```bash
# 1. Clone le repository
git clone https://github.com/syntaxe-devmessy/dark-gpt-ai.git
cd dark-gpt-ai

# 2. Lance l'installateur automatique
chmod +x install_darkgpt.sh
./install_darkgpt.sh
```

L'installateur va :

· Installer Python et les dépendances
· Télécharger le modèle Dolphin 2.9.1 (4-bit)
· Créer un service systemd
· Ouvrir le port 5000
· Démarrer l'API

---

🚀 Utilisation

```bash
# Démarrer le service
sudo systemctl start darkgpt

# Voir les logs
journalctl -u darkgpt -f

# Arrêter le service
sudo systemctl stop darkgpt

# Status
systemctl status darkgpt
```

Accès web : http://TON_IP_VPS:5000

---

📁 Structure du projet

```
dark-gpt-ai/
├── app.py                 # API principale
├── requirements.txt       # Dépendances
├── install_darkgpt.sh    # Script d'installation
├── start.sh              # Script de lancement
├── templates/            # Pages HTML
│   ├── index.html        # Accueil
│   ├── chat.html         # Interface chat
│   └── about.html        # À propos
└── static/               # CSS et JS
    ├── style.css
    └── script.js
```

---

🌐 Routes API

GET /api/status

Vérifier si le modèle est chargé

Réponse :

```json
{
  "status": "online",
  "model": "Dolphin 2.9.1 Mistral 7B",
  "loaded": true,
  "loading": false
}
```

POST /api/generate

Envoyer une question à l'IA

Requête :

```json
{
  "prompt": "Écris une fonction Python",
  "max_tokens": 500,
  "temperature": 0.7
}
```

Réponse :

```json
{
  "success": true,
  "response": "def hello():\n    print('Hello World')"
}
```

Exemple avec curl

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'
```

---

🗑️ Supprimer tout du VPS

Une seule commande pour tout supprimer :

```bash
sudo systemctl stop darkgpt && \
sudo systemctl disable darkgpt && \
sudo rm -f /etc/systemd/system/darkgpt.service && \
sudo systemctl daemon-reload && \
rm -rf ~/dark-gpt-ai && \
rm -rf ~/.cache/huggingface && \
sudo ufw delete allow 5000/tcp && \
echo "✅ Tout a été supprimé !"
```

Ou version plus simple (script)

```bash
wget -qO- https://raw.githubusercontent.com/syntaxe-devmessy/dark-gpt-ai/main/uninstall.sh | bash
```

---

⚙️ Configuration minimale

· VPS : 8GB RAM minimum
· Stockage : 10GB libre
· OS : Ubuntu 20.04+ / Debian 11+

---

📝 License

MIT License - Syntaxe Tech 2024

---

🔗 GitHub | Créé par Syntaxe Tech

```

## 🗑️ **Script de désinstallation `uninstall.sh`**

```bash
#!/bin/bash
# uninstall.sh - Supprime complètement Dark Gpt Ai du VPS

echo "🗑️  Suppression de Dark Gpt Ai..."

# Arrêter et supprimer le service
sudo systemctl stop darkgpt 2>/dev/null
sudo systemctl disable darkgpt 2>/dev/null
sudo rm -f /etc/systemd/system/darkgpt.service
sudo systemctl daemon-reload

# Supprimer les fichiers
rm -rf ~/dark-gpt-ai
rm -rf ~/.cache/huggingface

# Fermer le port firewall
sudo ufw delete allow 5000/tcp 2>/dev/null

# Nettoyer les processus
pkill -f "python.*app.py" 2>/dev/null

echo "✅ Dark Gpt Ai a été complètement supprimé !"
echo "📝 Pour réinstaller : git clone https://github.com/syntaxe-devmessy/dark-gpt-ai.git"
```

Rends-le exécutable :

```bash
chmod +x uninstall.sh
```

📋 Commandes à retenir

Action Commande
Installer git clone https://github.com/syntaxe-devmessy/dark-gpt-ai.git && cd dark-gpt-ai && ./install_darkgpt.sh
Désinstaller wget -qO- https://raw.githubusercontent.com/syntaxe-devmessy/dark-gpt-ai/main/uninstall.sh \| bash
Voir logs journalctl -u darkgpt -f
Tester API curl http://localhost:5000/api/status

C'est simple, propre et efficace ! 🚀
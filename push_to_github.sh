#!/bin/bash

# Script pour pousser tous les fichiers sur GitHub

echo "🚀 Push de Dark Gpt Ai sur GitHub..."
echo ""

# Initialiser git si nécessaire
if [ ! -d .git ]; then
    git init
    echo "✅ Git initialisé"
fi

# Ajouter tous les fichiers
git add .

# Commit
echo "📝 Création du commit..."
read -p "Message de commit (par défaut: 'Update Dark Gpt Ai'): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Update Dark Gpt Ai"
fi

git commit -m "$commit_msg"

# Push
echo "☁️ Push vers GitHub..."
git push -u origin main

echo ""
echo "✅ Fait ! Voir: https://github.com/syntaxe-devmessy/dark-gpt-ai"
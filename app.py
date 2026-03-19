import os
import torch
import threading
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
from datetime import datetime

# Configuration
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales
model = None
tokenizer = None
model_loaded = False
loading_started = False

# 🔥 MODÈLE PUBLIC QUI MARCHE PARFAITEMENT
MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'model': 'Phi-3 Mini',
        'loaded': model_loaded,
        'loading': loading_started,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    global model, tokenizer, model_loaded
    
    if not model_loaded:
        if not loading_started:
            threading.Thread(target=load_model).start()
        return jsonify({
            'success': False,
            'error': 'Modèle en cours de chargement',
            'status': 'loading'
        }), 202
    
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 500)
    temperature = data.get('temperature', 0.7)
    
    if not prompt:
        return jsonify({'error': 'Prompt requis'}), 400
    
    try:
        # Format pour Phi-3
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        # Tokenizer
        inputs = tokenizer.apply_chat_template(
            messages, 
            return_tensors="pt", 
            return_dict=True
        ).to(model.device)
        
        # Génération
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Décoder la réponse
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Nettoyer (enlever le prompt)
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>")[-1].strip()
        
        return jsonify({
            'success': True,
            'response': response,
            'model': 'Phi-3 Mini'
        })
        
    except Exception as e:
        logger.error(f"Erreur: {e}")
        return jsonify({'error': str(e)}), 500

def load_model():
    global model, tokenizer, model_loaded, loading_started
    loading_started = True
    
    try:
        logger.info("🚀 Chargement de Microsoft Phi-3 Mini...")
        logger.info("⚡ Modèle 3.8B optimisé pour 8GB RAM")
        
        # Charger le tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME, 
            trust_remote_code=True
        )
        
        # Ajouter un token de padding si nécessaire
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Charger le modèle
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        # Mode évaluation
        model.eval()
        
        model_loaded = True
        logger.info("✅ Modèle Phi-3 Mini chargé avec succès!")
        
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        loading_started = False

if __name__ == '__main__':
    logger.info("🚀 Démarrage de Dark Gpt Ai avec Phi-3 Mini")
    threading.Thread(target=load_model).start()
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
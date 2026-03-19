import os
import torch
import threading
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
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

# Configuration du modèle Dolphin 2.9.1 4-bit
MODEL_NAME = "cognitivecomputations/dolphin-2.9.1-mistral-7b"

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
        'model': 'Dolphin 2.9.1 Mistral 7B',
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
        return jsonify({'error': 'Modèle en cours de chargement'}), 202
    
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 500)
    temperature = data.get('temperature', 0.7)
    top_p = data.get('top_p', 0.95)
    
    if not prompt:
        return jsonify({'error': 'Prompt requis'}), 400
    
    try:
        messages = [{"role": "user", "content": prompt}]
        text = tokenizer.apply_chat_template(messages, tokenize=False)
        inputs = tokenizer(text, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=top_p,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if "[/INST]" in response:
            response = response.split("[/INST]")[-1].strip()
        
        return jsonify({
            'success': True,
            'response': response,
            'model': 'Dolphin 2.9.1'
        })
        
    except Exception as e:
        logger.error(f"Erreur: {e}")
        return jsonify({'error': str(e)}), 500

def load_model():
    global model, tokenizer, model_loaded, loading_started
    loading_started = True
    
    try:
        logger.info("🚀 Chargement de Dolphin 2.9.1 Mistral 7B (4-bit)...")
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True
        )
        
        model_loaded = True
        logger.info("✅ Modèle chargé avec succès!")
        
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        loading_started = False

if __name__ == '__main__':
    threading.Thread(target=load_model).start()
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
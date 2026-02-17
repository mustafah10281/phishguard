from flask import Flask, request, jsonify, render_template
import re
from urllib.parse import urlparse

app = Flask(__name__)

def check_url_safety(url):
    """Advanced URL checking with multiple rules"""
    score = 0
    reasons = []
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        full_url = url.lower()
        
        # RULE 1: Check for IP address (score 30)
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        if re.search(ip_pattern, domain):
            score += 30
            reasons.append("Uses IP address instead of domain name")
        
        # RULE 2: Check URL length (score 20)
        if len(url) > 75:
            score += 20
            reasons.append("Unusually long URL")
        
        # RULE 3: Check for @ symbol (score 25)
        if '@' in url:
            score += 25
            reasons.append("Contains @ symbol - hides real destination")
        
        # RULE 4: Check for HTTPS (score 10 if missing)
        if parsed.scheme != 'https':
            score += 10
            reasons.append("Not using HTTPS")
        
        # RULE 5: Suspicious keywords (score 15 each)
        suspicious_words = [
            'login', 'signin', 'verify', 'secure', 'account',
            'update', 'confirm', 'banking', 'password', 'credential',
            'verification', 'unlock', 'restore', 'limited', 'suspend'
        ]
        
        # Count suspicious words
        suspicious_count = 0
        for word in suspicious_words:
            if word in full_url:
                suspicious_count += 1
                if suspicious_count <= 3:  # Only add first 3 as reasons
                    reasons.append(f"Contains suspicious word: '{word}'")
        
        if suspicious_count > 0:
            score += suspicious_count * 15
        
        # RULE 6: Multiple subdomains (score 15)
        if domain.count('.') > 3:
            score += 15
            reasons.append("Too many subdomains")
        
        # RULE 7: Numbers in domain (score 10)
        if re.search(r'\d', domain):
            score += 10
            reasons.append("Contains numbers in domain")
        
        # RULE 8: Hyphens in domain (score 10)
        if '-' in domain:
            score += 10
            reasons.append("Contains hyphens in domain")
        
        # RULE 9: URL shortening services (score 20)
        shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 'ow.ly', 'is.gd', 'buff.ly', 'short.link']
        for short in shorteners:
            if short in domain:
                score += 20
                reasons.append(f"Uses URL shortener: {short}")
                break
        
        # RULE 10: Multiple forward slashes (score 15)
        if url.count('/') > 6:
            score += 15
            reasons.append("Multiple redirects")
        
        # RULE 11: Brand names in suspicious context (score 25)
        brands = ['paypal', 'apple', 'amazon', 'microsoft', 'netflix', 'chase', 'wellsfargo', 'facebook', 'instagram', 'gmail']
        for brand in brands:
            if brand in domain:
                # Check if it's trying to impersonate a brand
                domain_parts = domain.replace('www.', '').split('.')
                main_part = domain_parts[0] if domain_parts else ''
                
                # If brand is in domain but not the main part, it's suspicious
                if brand != main_part and any(word in domain for word in ['secure', 'verify', 'login', 'account', 'help']):
                    score += 25
                    reasons.append(f"Possible {brand} impersonation")
                    break
        
        # RULE 12: Too many dots in domain (score 15)
        if domain.count('.') >= 3:
            score += 15
            if "Too many subdomains" not in reasons:
                reasons.append("Unusual domain structure")
        
        # RULE 13: Check for common phishing TLDs (score 10)
        suspicious_tlds = ['.xyz', '.top', '.club', '.online', '.site', '.win', '.bid']
        for tld in suspicious_tlds:
            if domain.endswith(tld):
                score += 10
                reasons.append(f"Suspicious TLD: {tld}")
                break
        
        # RULE 14: Check for misspelled brand names (score 30)
        misspellings = [
            'paypall', 'paypal-security', 'pay-pal', 'appIe', 'microsft',
            'amaz0n', 'faceboook', 'gmaill', 'whatsapp-web'
        ]
        for miss in misspellings:
            if miss in domain:
                score += 30
                reasons.append(f"Misspelled brand name: {miss}")
                break
        
    except Exception as e:
        print(f"Error checking URL: {e}")
    
    # Determine if phishing (lower threshold to 30)
    is_phishing = score >= 30
    
    # Cap confidence at 100
    confidence = min(score, 100)
    
    # Risk level
    if confidence >= 70:
        risk = "HIGH"
    elif confidence >= 40:
        risk = "MEDIUM"
    elif confidence >= 20:
        risk = "LOW"
    else:
        risk = "MINIMAL"
    
    # Remove duplicate reasons
    unique_reasons = []
    for r in reasons:
        if r not in unique_reasons:
            unique_reasons.append(r)
    
    return {
        'is_phishing': is_phishing,
        'confidence': confidence,
        'risk': risk,
        'score': score,
        'reasons': unique_reasons[:5]  # Max 5 reasons
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'No URL provided'})
    
    # Add http:// if missing
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    result = check_url_safety(url)
    return jsonify(result)

if __name__ == '__main__':
    print("🚀 PhishGuard Advanced Starting...")
    print("📱 Open http://localhost:5000")
    app.run(debug=True, port=5000)
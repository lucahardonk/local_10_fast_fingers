from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///typing_test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Word list
WORD_LIST = [
    "about", "above", "add", "after", "again", "air", "all", "almost", "along", "also", "always", 
    "America", "an", "and", "animal", "another", "answer", "any", "are", "around", "as", "ask", 
    "at", "away", "back", "be", "because", "been", "before", "began", "begin", "being", "below", 
    "between", "big", "book", "both", "boy", "but", "by", "call", "came", "can", "car", "carry", 
    "change", "children", "city", "close", "come", "could", "country", "cut", "day", "did", 
    "different", "do", "does", "don't", "down", "each", "earth", "eat", "end", "enough", "even", 
    "every", "example", "eye", "face", "family", "far", "father", "feet", "few", "find", "first", 
    "follow", "food", "for", "form", "found", "four", "from", "get", "girl", "give", "go", "good", 
    "got", "great", "group", "grow", "had", "hand", "hard", "has", "have", "he", "head", "hear", 
    "help", "her", "here", "high", "him", "his", "home", "house", "how", "idea", "if", "important", 
    "in", "Indian", "into", "is", "it", "its", "it's", "just", "keep", "kind", "know", "land", 
    "large", "last", "later", "learn", "leave", "left", "let", "letter", "life", "light", "like", 
    "line", "list", "little", "live", "long", "look", "made", "make", "man", "many", "may", "me", 
    "mean", "men", "might", "mile", "miss", "more", "most", "mother", "mountain", "move", "much", 
    "must", "my", "name", "near", "need", "never", "new", "next", "night", "no", "not", "now", 
    "number", "of", "off", "often", "oil", "old", "on", "once", "one", "only", "open", "or", 
    "other", "our", "out", "over", "own", "page", "paper", "part", "people", "picture", "place", 
    "plant", "play", "point", "put", "question", "quick", "quickly", "quite", "read", "really", 
    "right", "river", "run", "said", "same", "saw", "say", "school", "sea", "second", "see", 
    "seem", "sentence", "set", "she", "should", "show", "side", "small", "so", "some", "something", 
    "sometimes", "song", "soon", "sound", "spell", "start", "state", "still", "stop", "story", 
    "study", "such", "take", "talk", "tell", "than", "that", "the", "their", "them", "then", 
    "there", "these", "they", "thing", "think", "this", "those", "thought", "three", "through", 
    "time", "to", "together", "too", "took", "tree", "try", "turn", "two", "under", "until", 
    "up", "us", "use", "very", "walk", "want", "was", "watch", "water", "way", "we", "well", 
    "went", "were", "what", "when", "where", "which", "while", "white", "who", "why", "will", 
    "with", "without", "word", "work", "world", "would", "write", "year", "you", "young", "your",
    "able", "about", "above", "across", "act", "actually", "add", "against", "age", "ago", "agree",
    "ahead", "allow", "almost", "alone", "already", "although", "among", "amount", "appear", "area",
    "arm", "arrive", "art", "attack", "attention", "avoid", "baby", "bad", "bag", "ball", "bank",
    "base", "basic", "beat", "beautiful", "become", "bed", "behind", "believe", "benefit", "best",
    "better", "beyond", "bit", "black", "blood", "blue", "board", "body", "born", "break", "bring",
    "brother", "build", "building", "business", "buy", "camera", "campaign", "cancer", "candidate",
    "capital", "card", "care", "career", "case", "catch", "cause", "cell", "center", "central",
    "century", "certain", "certainly", "chair", "challenge", "chance", "character", "charge", "check",
    "child", "choice", "choose", "church", "citizen", "claim", "class", "clear", "clearly", "coach",
    "cold", "collection", "college", "color", "common", "community", "company", "compare", "computer",
    "concern", "condition", "conference", "Congress", "consider", "consumer", "contain", "continue",
    "control", "cost", "court", "cover", "create", "crime", "cultural", "culture", "cup", "current",
    "customer", "dark", "data", "daughter", "dead", "deal", "death", "debate", "decade", "decide",
    "decision", "deep", "defense", "degree", "Democrat", "democratic", "describe", "design", "despite",
    "detail", "determine", "develop", "development", "die", "difference", "dinner", "direction",
    "director", "discover", "discuss", "discussion", "disease", "doctor", "dog", "door", "draw",
    "dream", "drive", "drop", "drug", "during", "early", "east", "easy", "economic", "economy",
    "edge", "education", "effect", "effort", "eight", "either", "election", "else", "employee",
    "energy", "enjoy", "entire", "environment", "environmental", "especially", "establish", "even",
    "evening", "event", "ever", "everybody", "everyone", "everything", "evidence", "exactly", "exist",
    "expect", "experience", "expert", "explain", "fail", "fall", "fast", "federal", "feel", "feeling",
    "field", "fight", "figure", "fill", "film", "final", "finally", "financial", "finger", "finish",
    "fire", "firm", "five", "floor", "fly", "focus", "foot", "force", "foreign", "forget", "former",
    "forward", "free", "friend", "full", "fund", "future", "game", "garden", "gas", "general",
    "generation", "glass", "goal", "green", "ground", "gun", "guy", "hair", "half", "hang", "happen",
    "happy", "hate", "health", "healthy", "heat", "heavy", "help", "herself", "himself", "history",
    "hit", "hold", "hope", "hospital", "hot", "hotel", "hour", "huge", "human", "hundred", "husband",
    "image", "imagine", "impact", "improve", "include", "including", "increase", "indeed", "indicate",
    "individual", "industry", "information", "inside", "instead", "institution", "interest",
    "interesting", "international", "interview", "investment", "involve", "issue", "item", "itself",
    "job", "join", "key", "kid", "kill", "kitchen", "knowledge", "language", "law", "lawyer", "lay",
    "lead", "leader", "leg", "legal", "less", "level", "lie", "likely", "local", "lose", "loss",
    "lot", "love", "low", "machine", "magazine", "main", "maintain", "major", "majority", "manage",
    "management", "manager", "market", "marriage", "material", "matter", "maybe", "measure", "media",
    "medical", "meet", "meeting", "member", "memory", "mention", "message", "method", "middle",
    "military", "million", "mind", "minute", "mission", "model", "modern", "moment", "money", "month",
    "morning", "mouth", "Mrs", "natural", "nature", "necessary", "network", "news", "newspaper",
    "nice", "north", "note", "nothing", "notice", "occur", "offer", "office", "officer", "official",
    "oh", "ok", "operation", "opportunity", "option", "order", "organization", "others", "outside",
    "owner", "pain", "painting", "parent", "particular", "particularly", "partner", "party", "pass",
    "past", "patient", "pattern", "pay", "peace", "per", "perform", "performance", "perhaps", "period",
    "person", "personal", "phone", "physical", "pick", "piece", "plan", "player", "PM", "policy",
    "political", "politics", "poor", "popular", "population", "position", "positive", "possible",
    "power", "practice", "prepare", "present", "president", "pressure", "pretty", "prevent", "price",
    "private", "probably", "problem", "process", "produce", "product", "production", "professional",
    "professor", "program", "project", "property", "protect", "prove", "provide", "public", "pull",
    "purpose", "push", "quality", "raise", "range", "rate", "rather", "reach", "realize", "reason",
    "receive", "recent", "recently", "recognize", "record", "red", "reduce", "reflect", "region",
    "relate", "relationship", "religious", "remain", "remember", "remove", "report", "represent",
    "Republican", "require", "research", "resource", "respond", "response", "responsibility", "rest",
    "result", "return", "reveal", "rich", "rise", "risk", "road", "rock", "role", "room", "rule",
    "safe", "sale", "save", "scene", "scientist", "score", "season", "seat", "seek", "sell", "send",
    "senior", "sense", "series", "serious", "serve", "service", "seven", "several", "sex", "sexual",
    "shake", "share", "shoot", "short", "shot", "shoulder", "sign", "significant", "similar", "simple",
    "simply", "since", "sing", "single", "sister", "sit", "site", "situation", "six", "size", "skill",
    "skin", "sleep", "smile", "social", "society", "soldier", "somebody", "someone", "son", "sort",
    "source", "south", "southern", "space", "speak", "special", "specific", "speech", "spend", "sport",
    "spring", "staff", "stage", "stand", "standard", "star", "station", "stay", "step", "stock",
    "store", "strategy", "street", "strong", "structure", "student", "stuff", "style", "subject",
    "success", "successful", "suddenly", "suffer", "suggest", "summer", "support", "sure", "surface",
    "system", "table", "task", "tax", "teach", "teacher", "team", "technology", "television", "ten",
    "tend", "term", "test", "thank", "themselves", "theory", "these", "thousand", "threat", "throw",
    "thus", "today", "tonight", "top", "total", "tough", "toward", "town", "trade", "traditional",
    "training", "travel", "treat", "treatment", "trial", "trip", "trouble", "true", "truth", "type",
    "unit", "upon", "usually", "value", "various", "victim", "view", "violence", "visit", "voice",
    "vote", "wait", "wall", "war", "weapon", "wear", "week", "weight", "west", "western", "whatever",
    "whether", "whole", "whom", "whose", "wide", "wife", "win", "wind", "window", "wish", "within",
    "woman", "wonder", "worker", "worry", "worse", "worst", "worth", "yeah", "yes", "yet", "yourself"
]
# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tests = db.relationship('TestResult', backref='user', lazy=True)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in seconds
    correct_words = db.Column(db.Integer, nullable=False)
    wrong_words = db.Column(db.Integer, nullable=False)
    total_words = db.Column(db.Integer, nullable=False)
    wpm = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    
    session['username'] = username
    session['user_id'] = user.id
    return jsonify({'success': True})

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/test/<int:duration>')
def test(duration):
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if duration not in [60, 120, 300, 600]:
        duration = 60
    
    return render_template('test.html', duration=duration, username=session['username'])

@app.route('/get_words')
def get_words():
    # Generate 1000 random words for the test
    words = random.choices(WORD_LIST, k=1000)
    return jsonify({'words': words})

@app.route('/save_result', methods=['POST'])
def save_result():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    
    result = TestResult(
        user_id=session['user_id'],
        duration=data['duration'],
        correct_words=data['correct_words'],
        wrong_words=data['wrong_words'],
        total_words=data['total_words'],
        wpm=data['wpm'],
        accuracy=data['accuracy']
    )
    
    db.session.add(result)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    results = TestResult.query.filter_by(user_id=session['user_id']).order_by(TestResult.created_at.desc()).all()
    
    history_data = [{
        'id': r.id,
        'date': r.created_at.strftime('%Y-%m-%d %H:%M'),
        'duration': r.duration,
        'correct_words': r.correct_words,
        'wrong_words': r.wrong_words,
        'total_words': r.total_words,
        'wpm': round(r.wpm, 2),
        'accuracy': round(r.accuracy, 2)
    } for r in results]
    
    return render_template('history.html', history=history_data, username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

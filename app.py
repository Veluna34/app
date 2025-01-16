from flask import Flask, redirect, url_for, render_template, request, session, flash, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from bs4 import BeautifulSoup
from functools import wraps
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO
import time
from threading import Thread
from pytrends.request import TrendReq
import requests



app = app = Flask(__name__, template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins
API_KEY = "abcd1234efgh"  # This is the value
API_URL = "https://api.bing.microsoft.com/v7.0/search"

headers = {"Ocp-Apim-Subscription-Key": API_KEY}
params = {"q": "New Jersey", "count": 10}

response = requests.get(API_URL, headers=headers, params=params)





app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Port 587 is recommended for SendGrid with TLS
app.config['MAIL_USE_TLS'] = True  # Use TLS
app.config['MAIL_USE_SSL'] = False  # Don't use SSL
app.config['MAIL_USERNAME'] = 'redratgames1@gmail.com'  # Use 'apikey' as the username (not your email)
app.config['MAIL_PASSWORD'] = 'xeeo gdet edul qfvs'  # Use your SendGrid API key here
app.config['MAIL_DEFAULT_SENDER'] = '@example.com'  # Set the default sender's email

mail = Mail(app)

app.secret_key = 'Aiden Figueroa'  # Required for session management

DATABASE = 'account.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    with sqlite3.connect('account.db') as conn:
        cursor = conn.cursor()

        # Create the 'users' table if it doesn't exist
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        # Optionally insert a sample user (if you want to add one)
        # First, check if the user exists
        cursor.execute('SELECT * FROM users WHERE username = ?', ('fire',))
        user = cursor.fetchone()

        if user is None:  # Insert user if not already present
            cursor.execute(''' 
                INSERT INTO users (username, email, password) 
                VALUES (?, ?, ?)
            ''', ('fire', 'fire@example.com', generate_password_hash('securepassword')))
        else:  # Update user if already present
            cursor.execute(''' 
                UPDATE users 
                SET email = ?, password = ?
                WHERE username = ?
            ''', ('fire@example.com', generate_password_hash('newpassword'), 'fire'))

        # Commit changes to the database
        conn.commit()

        print("Database and table created successfully.")

init_db()

TEMPLATES = [
    'doublespeak.html',
    'elephantCollection.html',
    'Fun.html',
    'google.html',
    'henry.html',
    'homepage.html',
    'inno.html',
    'io.html',
    'juicy.html',
    'multiplayer.html',
    'neilsGames.html',
    'newgrounds.html',
    'online.html',
    'original.html',
    'orteil.html',
    'otto.html',
    'phoboslab.html',
    'popular.html',
    'recommendations.html',
    'retro.html',
    'wix.html',
    'ai.html',
    'art.html',
    'artists.html',
    'business.html',
    'clothing.html',
    'coming.html',
    'designers.html',
    'developers.html',
    'electronics.html',
    'encyclopedia.html',
    'entertainment.html',
    'luxury.html',
    'math.html',
    'music.html',
    'news.html',
    'office.html',
    'professional.html',
    'personal.html',
    'projects.html',
    'reading.html',
    'retail.html',
    'shows.html',
    'socials.html',
    'users.html',
    'video.html',
    'workspace.html',
    'submitted.html',
    'insurance.html',
    'invest.html',
    'currency.html',
    'gambling.html',
    'credit.html',
    'financial.html',
    'supply.html',
    'delivery.html',
    'marketplace.html',
    'banks.html',
    'internet.html',
    'fitness.html',
    'mind.html',
    'hotels.html',
    'travelling.html',
    'groceries.html'
]

TEMPLATE_TITLES = {
    'wix.html': 'Wix Games (Games)',
    'online.html': 'Online Games (Games)',
    'ai.html':'Artificial Intelligence (Productivity)',
    'art.html':'Art Design (Design)',
    'artists.html':'Music Creation (Design)',
    'business.html':'productivity Tools (Productivity)',
    'clothing.html':'Clothing Stores (Shopping)',
    'collections.html':'Browser Game Collections (Games)',
    'designers.html':'Design Tools (Design)',
    'developers.html':'Developer Tools (Design)',
    'doublespeak.html':'Double Speak Games (Games)',
    'electronics.html':'Electronic Stores (Shopping)',
    'elephantCollection.html':'The Elephant Collection Games',
    'encyclopedia.html':'Information Sources (Information)',
    'entertainment.html':'Entertainment Stores (Shopping)',
    'Fun.html':'Other Fun Websites (Games)',
    'google.html':'Games From Google (Games)',
    'henry.html':'The Henry Stickmin Collection (Games)',
    'inno.html':'Inno Games (Games)',
    'io.html':'Popular .IO Games (Games)',
    'juicy.html':'Juicy Beast (Games)',
    'luxury.html':'Luxury Highend Brands (Shopping)',
    'math.html':'Math & Science Tools (Productivity)',
    'multiplayer.html':'Popular Multiplayer Games (Games)',
    'music.html':'Streaming Services For Music (Entertainment)',
    'neilsGames.html':'Games From Neil.Fun (Games)',
    'newgrounds.html':'The Best From Newgrounds (Games)',
    'news.html':'News Sources (Information)',
    'nyt.html':'Games From The New York Times (Games)',
    'office.html':'Microsoft Office (Productivity)',
    'online.html':'Popular Online Browser Games (Games)',
    'orteil.html':'Games From Orteil (Games)',
    'otto.html':'Game From Otto Ojola (Games)',
    'personal.html':'Social Media For Personal Use (Social Media)',
    'phoboslab.html':'Games From PhobosLab (Games)',
    'popular.html':'Popular Browser Games (Games)',
    'professional.html':'Social Media For Work',
    'project.html':'Crafts & Rennovations (Work)',
    'reading.html':'Stream Your Books (Entertainment)',
    'recommendations.html':'Games I Recommend',
    'retail.html':'Retail Stores (Shopping)',
    'retro.html':'Retro Games (Games)',
    'shows.html':'Strem Your Shows (Media)',
    'Timeline.html':'The Timeline (Games)',
    'users.html':'Independant Web Devlopers',
    'video.html':'For Video Editing (Design)',
    'workspace.html': 'Googe Workspace (Productivity)',
    'homepage.html': 'The Red Rat Web',
    'submitted.html':'User Submitted Websites (Community)',
    'insurance.html': 'Insurance Services (Fincances)',
    'invest.html': 'Invest Your Money (Finances)',
    'banks.html': 'Online Banking (Finances)',
    'currency.html': 'Online Currencies (Finances)',
    'gambling.html': 'Gambling & Betting (Finances)',
    'credit.html': 'Credit Cards/Services (Finances)',
    'financial.html': 'General Financial Tools (Finances)',
    'delivery.html': 'Delivery/Transportation Services',
    'supply.html': 'Supplies For Home & DIY Projects (Shopping)',
    'marketplace.html': 'Marketplaces (Shopping)',
    'internet.html': 'Internet Services',
    'fitness.html': 'Physical Health',
    'mind.html': 'Mental Health',
    'hotels.html': 'Places To Stay',
    'travelling.html': 'Buy Your Flight',
    'groceries.html': 'Grocery Stores (Shopping)'
}

TEST_MODE = True  # Set to False for real-time data fetching


def fetch_trends(test_mode=True):
    """
    Fetch trends data based on the mode:
    - Test mode returns static data for development.
    - Production mode fetches real-time data using the Bing Search API.
    """
    if TEST_MODE==True:
        # Return static data for testing
        return {
            'Websites': ['Google', 'YouTube', 'Facebook', 'Amazon', 'Wikipedia',
                         'Instagram', 'Twitter', 'Reddit', 'ChatGPT', 'WhatsApp'],
            'Search Volume': [90, 85, 80, 75, 70, 65, 60, 55, 50, 45]
        }
    else:
        # Fetch real-time data using Bing API
        return fetch_real_data()

def fetch_real_data():
    """
    Fetch real-time data from the Bing Search API.
    """
    try:
        keywords = ['google', 'youtube', 'facebook', 'amazon', 'wikipedia',
                    'instagram', 'twitter', 'reddit', 'chatgpt', 'whatsapp']
        
        search_volumes = []

        for keyword in keywords:
            # Prepare API request
            headers = {"Ocp-Apim-Subscription-Key": API_KEY}
            params = {"q": keyword, "count": 1}  # Query and limit results
            
            # Send request to Bing Search API
            response = requests.get(API_URL, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                
                # Example metric: Count the number of search results returned
                search_volume = len(data.get("webPages", {}).get("value", []))
                search_volumes.append(search_volume)
            else:
                # Log and fallback for errors
                print(f"Error fetching data for {keyword}: {response.status_code}")
                search_volumes.append(0)

        # Return data in the format expected by the front-end
        return {'Websites': keywords, 'Search Volume': search_volumes}

    except Exception as e:
        print(f"Error fetching real-time data: {e}")
        # Fallback in case of an error
        return {'Websites': [], 'Search Volume': []}

    
def fetch_and_emit_data(test_mode=True):
    """Fetch trends and emit the data to all connected clients."""
    while True:
        # Fetch data (either test data or real-time data)
        data = fetch_trends(test_mode)
        
        # Emit the data to all connected clients using Socket.IO
        socketio.emit('update_data', data)
        
        # Use a short delay for testing, longer delay for production
        time.sleep(30 if test_mode else 28800)  # 28800 seconds = 8 hours for production


@socketio.on('connect')
def handle_connect():
    print("Client connected!")
    # Start the data-fetching thread
    thread = Thread(target=fetch_and_emit_data, args=(True,))  # Set to True for testing mode
    thread.start()


# Function to extract alt texts from templates
def extract_alt_texts(template_name):
    """Extracts alt texts from image tags in a given template file"""
    alt_texts = []
    try:
        template_file_path = os.path.join('templates', template_name)
        with open(template_file_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Extract all image tags and get the alt attribute
        for img in soup.find_all('img'):
            alt = img.get('alt')
            if alt:
                normalized_alt = alt.replace(' ', '')
                alt_texts.append(alt)
    except Exception as e:
        print(f"Error processing {template_name}: {e}")
    return alt_texts

# Preprocess all templates to extract alt text data
alt_text_data = {}
for template in TEMPLATES:
    alt_text_data[template] = extract_alt_texts(template)

@app.route("/", methods=["GET", "POST"])
def signInPage():
    return render_template('signInPage.html')



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session)  # Print session to see its content
        # Check if the user is logged in by checking the session
        if 'username' not in session:
            flash("You must be signed in to access this page.", "error")
            return redirect(url_for('signInPage'))  # Redirect tvbgnho sign in page if not logged in
        return f(*args, **kwargs)
    return decorated_function


@app.route('/search', methods=['GET', 'POST'])
def search():
    alt_text_data = {
        'ai.html': ['Artificial Intelligence', 'A.I.', 'ai', 'A.I. Tools', 'ai tools', 'tools', 'working', 'productivity', 'effeciency'],
        'art.html': ['art', 'deign', 'art tools', 'working', 'art deign', 'work', 'tools', 'media'],
        'artists.html': ['art', 'deign', 'art tools', 'working', 'art deign', 'media'],
        'artists.html': ['music', 'music production', 'music design', 'working', 'dsign tools', 'tools', 'media'],
        'business.html': ['general', 'productivity','working', 'effeciancy'],
        'clothing.html': ['clothes', 'clothing','online shops', 'online shopping', 'online stores'],
        'collections.html': ['game collections', 'browser games','entertainment' 'media'],
        'designers.html': ['tools', 'general design','working'],
        'developers.html': ['developers', 'coding','code', 'programming', 'programs', 'work', 'tools', 'design'],
        'doublespeak.html': ['doublespeak games', 'browser games','entertainment', 'media'],
        'electronics.html': ['electronics', 'online shops','online shopping', 'devices'],
        'elephantCollection.html': ['browser games', 'Elephant collection','entertainment','media'],
        'encyclopedia.html': ['information', 'encyclopedias','work', 'tools', 'research'],
        'entertainment.html': ['entertainment', 'online shops','online shopping', 'games', 'media', 'books', 'music', 'comics', 'media'],
        'Fun.html': ['other Websites', 'fun','games', 'reccomendations'],
        'google.html': ['browser games', 'google','entertainment', 'media'],
        'henry.html': ['henry stickmin collection', 'entertainment','browser games', 'media'],
        'information.html': ['information', 'news','entertainment', 'media', 'research'],
        'inno.html': ['Inno Games', 'Browser Games','entertainment', 'media'],
        'i0.html': ['Popular IO Games', 'Browser Games','entertainment', 'media'],
        'juicy.html': ['Juicy Games', 'Browser Games','entertainment', 'media'],
        'luxury.html': ['Luxury Stores', 'High end stores','online shopping', 'online shops', 'clothes', 'clothing'],
        'math.html': ['Math', 'science','tools', 'work', 'math tools', 'science tools', 'calculators', 'graphing', 'productivity'],
        'multiplayer.html': ['popular coop games', 'popular multiplayer games','browser games', 'entertainment', 'media'],
        'music.html': ['music', 'streaming','podcasts', 'entertainment', 'media'],
        'neilsGames.html': ['Neil.fun', 'Browser Games','entertainment', 'media'],
        'newgorunds.html': ['popualar games from Newgrounds', 'Browser games','entertainment', 'media'],
        'news.html': ['information', 'news','entertainment', 'media', 'research'],
        'nyt.html': ['games from the new york times','entertainment', 'media', 'browser games'],
        'office.html': ['microsoft office','work', 'tools', 'productivity'],
        'online.html': ['popular online games','browser games', 'media', 'entertainment'],
        'original.html': ['original games','browser games', 'media', 'entertainment'],
        'orteil.html': ['games from orteil','browser games', 'media', 'entertainment', 'orteil games'],
        'otto.html': ['games from otto ojala','browser games', 'media', 'entertainment', 'Otto ojala games'],
        'personal.html': ['personal social media','media', 'entertainment', 'work', 'tools'],
        'phoboslab.html': ['phoboslab games','media', 'entertainment','browser games'],
        'popular.html': ['popular games','media', 'entertainment', 'browser games'],
        'professional.html': ['professional social meda','media', 'entertainment', 'work', 'tools'],
        'professional.html': ['professional social meda','media', 'entertainment', 'work', 'tools'],
        'projects.html': ['projects','online shopping', 'online shops', 'work', 'tools', 'arts and crafts'],
        'reading.html': ['streaming services' ,'books', 'reading', 'information', 'entertainment', 'media'],
        'reccomendations.html': ['games i recommend','recommendations', 'games', 'entertainment', 'media'],
        'retail.html': ['retail stores','online shopping', 'online shops', 'retail shops'],
        'retro.html': ['retro games','popular games', 'browser games', 'entertainment', 'media'],
        'shows.html': ['shows','movies', 'videos', 'streaming services', 'streaming platforms', 'media', 'entertainment', 'tv', 't.v.', 'television'],
        'timeline.html': ['videos','music', 'games', 'information', 'research', 'media', 'entertainment', 'The Timeline'],
        'users.html': ['independant developers','websites', 'user cerated websites', 'other websites', 'media', 'math', 'calculus', 'health', 'working out', 'the gym', 'fitness'],
        'video.html': ['video editing','tools', 'videos', 'entertainment', 'media', 'design'],
        'wix.html': ['Wix Games', 'Browser Games', 'entertainment', 'media'],
        'workspace.html': ['Google Workspace', 'office tools', 'work', 'prodcutivity'],
        'submitted.html': ['user submitted websites', 'community', 'from users', 'people', 'from people'],
        'insurance.html': ['insurance', 'money', 'homeowner insurance', 'car insurance', 'home insurance', 'health insurance', 'auto insurance', 'finances', 'financial services', 'tools'],
        'invest.html': ['investments', 'investing', 'money', 'finances', 'financial services', 'tools', 'work'],
        'banks.html': ['banks', 'banking', 'money', 'finances', 'financial services', 'tools'],
        'currency.html': ['online currencies', 'online currency', 'money', 'finances', 'financial services','cryptocurrency', 'cryptocurrencies', 'tools'],
        'gambling.html': ['Gambling', 'Betting', 'money', 'finances', 'financial services','sports', 'casinos'],
        'credit.html': ['credit cards', 'tools', 'money', 'finances', 'financial services'],
        'financial.html': ['credit cards', 'tools', 'money', 'finances', 'financial services', 'general tools', 'currency'],
        'supply.html': ['supplies', 'supply', 'shopping', 'work', 'stores', 'home imporvement', 'tools', 'resources'],
        'delivery.html': ['delivery services', 'transportation', 'food', 'cars'],
        'marketplace.html': ['products', 'services', 'tools', 'design', 'games', 'entertainment', 'resources', 'marketplaces', 'general', 'work', 'media'],
        'internet.html': ['intenret services', 'phones', 'resources', 'work'],
        'fitness.html': ['fitness', 'gyms', 'tools', 'excercise', 'athletics', 'resources', 'health', 'work', 'yoga', 'pilates', 'classes'],
        'mind.html': ['mind', 'health', 'mental health', 'work', 'therapy', 'help', 'relaxation', 'services', 'tools'],
        'hotels.html': ['travelling', 'hotels', 'Places To Stay', 'work', 'vacation', 'relaxation', 'business'],
        'travelling.html': ['travel', 'travelling', 'flights', 'flying', 'airplanes', 'relaxation', 'business'],
        'groceries.html': ['Grocery Stores', 'Shopping', 'Groceries', 'food', 'supplies', 'health', 'supply' 'resources']
    }

    search_query = request.args.get('query', '').strip()

    if not search_query:
        flash("Please enter a search query.")
        return render_template('homepage.html', pages=[], query=search_query)

    matching_pages = []

    # Step 1: Check alt text data in the alt_text_data dictionary
    for template, alt_texts in alt_text_data.items():
        for alt_text in alt_texts:
            if search_query.lower() in alt_text.lower():  # Case-insensitive match
                if template not in matching_pages:
                    matching_pages.append(template)
                break  # Stop after finding one match for this template

    # Step 2: Check alt attributes in HTML templates (for templates in the TEMPLATES list)
    for template in TEMPLATES:
        # Get the file path of the template
        template_path = os.path.join('templates', template)  # Make sure the path is correct

        if os.path.exists(template_path):  # Check if the template file exists
            with open(template_path, 'r', encoding='utf-8') as f:
                # Parse the template HTML file with BeautifulSoup
                soup = BeautifulSoup(f, 'html.parser')

                # Find all elements with the 'alt' attribute
                images = soup.find_all(attrs={"alt": True})
                
                # Check if any 'alt' attribute contains the search query
                for img in images:
                    if search_query.lower() in img['alt'].lower():  # Case-insensitive match
                        if template not in matching_pages:
                            matching_pages.append(template)
                        break  # Stop after finding one match for this template

    # Step 3: Handle the results
    if len(matching_pages) == 1:
        return render_template(matching_pages[0])  # Render the single matched template

    if matching_pages:
        page_titles = [(template, TEMPLATE_TITLES.get(template, template)) for template in matching_pages]
        return render_template('search_results.html', pages=page_titles, query=search_query)

    flash("No results found.")
    return render_template('homepage.html', pages=[], query=search_query)




@app.route("/logout")
def logout():
    session.clear()
    flash("You Have Been Logged Out")
    return redirect(url_for('signInPage'))

@app.route("/data")
def data():
    return render_template('data.html')

@app.route('/view_template/<template_name>')
def view_template(template_name):
    try:
        # Render the selected template. You can also add additional context to this if needed.
        return render_template(template_name)
    except Exception as e:
        # If there is an error (e.g., template doesn't exist), show a flash message
        flash(f"Error rendering template: {e}")
        return redirect(url_for('homepage'))  # Redirect to homepage or any other fallback route


@app.route('/createaccount', methods=["GET", "POST"])
def createAccount():
    success = False  # Default to False
    if request.method == "POST":
        # Get the form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        try:
            with sqlite3.connect('account.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
                existing_user = cursor.fetchone()

                if existing_user:
                    flash("Username or email already exists. Please try again.", "error")
                    return render_template('createAccount.html')
            
                cursor.execute('''
                    INSERT INTO users (username, email, password)
                    VALUES (?, ?, ?)
                ''', (username, email, hashed_password))
                conn.commit()

                session['username'] = username  # Automatically log the user in
                session['email'] = email  # Automatically log the user in

            # Flash success message and redirect to the homepage
            flash("Account created successfully! Please log in.", "success")
            success = True  # Set success to True if login is successful
            return redirect(url_for('homepage'))  # Or wherever you want to go after successful signup

        
        except sqlite3.IntegrityError:  # Handle unique constraint violations (e.g., duplicate username or email)
            flash("Username or email already exists. Please try again.", "error")
        
    # If the request method is GET, render the create account form
    return render_template('createAccount.html', success=success)


# Route to handle sign in
@app.route('/signin', methods=['GET', "POST"])
def signin():
    if request.method == "POST":
        # Get the form data for login
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists and verify the password
        with sqlite3.connect('account.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result and check_password_hash(result[3], password):
                session['username'] = username  # Store the username in the session
                session['email'] = result[2]  # Assuming the email is in the 3rd column (index 2)
                flash("Successfully signed in!", "success")
                return redirect(url_for('homepage'))  # Redirect to the homepage
            else:
                flash("Invalid username or password. Please try again.", "error")
                return render_template('signIn.html')
        return render_template('signIn.html')
    return render_template('signIn.html')

def get_user_id(username):
    with sqlite3.connect('account.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    
@app.route('/get_user_websites', methods=['GET'])
def get_user_websites():
    if 'username' not in session:
        flash({'success': False, 'message': 'User not logged in.'}), 401
        return render_template('signInPage')

    user_id = get_user_id(session['username'])

    try:
        with sqlite3.connect('account.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT url, name, type FROM user_websites WHERE user_id = ?
            ''', (user_id,))
            websites = cursor.fetchall()

        # Group by type
        favorite_websites = [w for w in websites if w[2] == 'favorite']
        liked_websites = [w for w in websites if w[2] == 'liked']

        flash({
            'success': True,
            'favorites': favorite_websites,
            'liked': liked_websites
        })
        return render_template('profile.html')
    except Exception as e:
        flash({'success': False, 'message': str(e)}), 500
        return render_template('signInPage.html')




@app.route('/toggle_website', methods=['POST'])
def toggle_website():
    if 'username' not in session:
        flash('You need to sign in to perform this action.', 'error')
        return redirect(url_for('signInPage'))  # Redirect to the sign-in page if not logged in

    user_id = get_user_id(session['username'])
    website_url = request.json.get('url')
    website_name = request.json.get('name')
    website_type = request.json.get('type')

    if not all([user_id, website_url, website_name, website_type]):
        flash('Invalid data provided.', 'error')
        return redirect(url_for('profile'))  # Redirect to profile page if data is invalid

    try:
        with sqlite3.connect('account.db') as conn:
            cursor = conn.cursor()

            # Check if the website already exists for the user in the specified list (favorite or liked)
            cursor.execute('''
                SELECT * FROM user_websites
                WHERE user_id = ? AND url = ? AND type = ?
            ''', (user_id, website_url, website_type))
            existing = cursor.fetchone()

            if existing:
                # If website exists, remove it from the list
                cursor.execute('''
                    DELETE FROM user_websites
                    WHERE user_id = ? AND url = ? AND type = ?
                ''', (user_id, website_url, website_type))
                conn.commit()
                flash(f'Website removed from {website_type} list.', 'success')
            else:
                # If website does not exist, add it to the list
                cursor.execute('''
                    INSERT INTO user_websites (user_id, url, name, type)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, website_url, website_name, website_type))
                conn.commit()
                flash(f'Website added to {website_type} list.', 'success')

        # Fetch updated lists directly for rendering
        with sqlite3.connect('account.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT url, name FROM user_websites WHERE user_id = ? AND type = ?', (user_id, 'favorite'))
            favorite_websites = cursor.fetchall()
            cursor.execute('SELECT url, name FROM user_websites WHERE user_id = ? AND type = ?', (user_id, 'liked'))
            liked_websites = cursor.fetchall()

        # Build the updated HTML for favorite and liked websites
        favorite_html = render_template_string('''
            <ul>
                {% for website in websites %}
                    <li><a href="{{ website[0] }}" target="_blank">{{ website[1] }}</a></li>
                {% endfor %}
            </ul>
        ''', websites=favorite_websites)

        liked_html = render_template_string('''
            <ul>
                {% for website in websites %}
                    <li><a href="{{ website[0] }}" target="_blank">{{ website[1] }}</a></li>
                {% endfor %}
            </ul>
        ''', websites=liked_websites)

        # Return updated HTML for the lists
        return {'favorite_html': favorite_html, 'liked_html': liked_html}

    except sqlite3.IntegrityError as e:
        flash('Error updating the database.', 'error')
        return redirect(url_for('profile'))  # Redirect to the profile page if there is a database error





@app.route("/send_email", methods=['POST'])
def send_email():
    if request.method=='POST':
        name=request.form['name']
        email=session['email']
        subject=request.form['subject']
        message=request.form['message']
        username=session['username']

        if not email:
            flash("No email in session", 'danger')
            return redirect(url_for('signInPage'))
        
        user_message = Message(
            subject="Thank You For Contacting Me",  # Email subject
            sender=app.config['MAIL_USERNAME'],  # Sender email (your email)
            recipients=[email]  # Recipient email (user's email from session)
        )
        
        # Setting the body of the email
        user_message.body = f"Hi {username},\n\nThank you for submitting the message: {subject}.\n\n" \
                            f"We have received the following details:\n" \
                            f"Name: {name}\n" \
                            f"Message: {message}\n\n" \
                            f"I Will Respond Shortly\n\n" \
                            f"Best regards,\nRed Rat Games"
        
        # Send the email to the user
        mail.send(user_message)

        msg = Message(subject=subject,  # subject of the email
                      sender=app.config['MAIL_USERNAME'],  # sender's email
                      recipients=[email])  # recipient email(s)
        msg.body=f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)

        flash("Message Sent To My Email!", 'success')
    return redirect(url_for('homepage'))

def update_user_in_db(new_username, new_password, new_email, profile_image_path):
    current_email = session.get('email')  # Get the current user's email from session

    if current_email:
        # Connect to the SQLite database
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()

        # If the email is changed, check if the new email already exists (except for the current user)
        if new_email != current_email:
            cursor.execute('SELECT * FROM users WHERE email = ?', (new_email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash(f"Error: Email '{new_email}' is already in use.")
                return  # Do not proceed with the update if the email is already taken

        print(f"Attempting to update user {current_email} with new details.")
        
        # Hash the new password
        hashed_password = generate_password_hash(new_password)

        # Update the user's details in the database, including the profile image path
        sql = '''
        UPDATE users
        SET username = ?, password = ?, email = ?, profile_image = ?
        WHERE email = ?
        '''

        try:
            # Execute the update query
            cursor.execute(sql, (new_username, hashed_password, new_email, profile_image_path, current_email))
            conn.commit()
            flash("User updated successfully")

            # After the update is successful, update the session with the new username
            session['username'] = new_username  # Update session with new username

        except sqlite3.Error as e:
            flash(f"Error updating user: {e}")
            conn.rollback()

        finally:
            conn.close()

    else:
        flash("User not logged in.")

@app.route('/update_username', methods=['POST'])
def update_username():
    try:
        # Get the new username from the form or request
        new_username = request.form.get('username')  # Use request.form for non-JSON form data

        if new_username:
            # Update the username in the session
            session['username'] = new_username

            # Flash success message
            flash("Username updated successfully!", "success")
        else:
            flash("Invalid username", "error")
    except Exception as e:
        # Flash error message if something goes wrong
        flash(f"Error: {str(e)}", "error")
    
    # Redirect to the settings page (or wherever you want to show the flash message)
    return redirect(url_for('profile'))  # Adjust 
@app.route("/updateAccount", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        new_email = request.form['email']
        second_password = request.form['confirm-password']

        # Handle profile image upload
        profile_image = request.files.get('profileImage')

        if second_password != new_password:
            flash("Passwords Do Not Match")
            return render_template('settings.html')  # Redirect back to the settings page

        # Debug: Print to confirm the data is being received correctly
        print(f"Updating user with Username: {new_username}, Email: {new_email}")

        # If there's an uploaded image, save it
        if profile_image:
                # Secure the filename and save the image
                filename = secure_filename(profile_image.filename)
                image_path = os.path.join('static', 'profile_images', filename)  # Save in 'static/profile_images'
                profile_image.save(image_path)
                session['file-upload'] = f'/static/profile_images/{filename}'  # Store the relative image path in session
        else:
            session['file-upload'] = None  # No image uploaded, set it to None or use a default path
            image_path = None  # No image uploaded, keep it None or use a default path

        # Call the function to update user info in DB
        update_user_in_db(new_username, new_password, new_email, image_path)

        return redirect(url_for('homepage'))  # Redirect to homepage after successful update

    return 'Update page'
UPLOAD_FOLDER = os.path.join('static', 'profile_images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/updateProfileImage', methods=['POST'])
def update_profile_image():
    # Check if the form has an image file
    profile_image = request.files.get('profileImage')
    if profile_image:
        # Secure the filename and save the image
        filename = secure_filename(profile_image.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        profile_image.save(file_path)

        # Update the session with the new profile image path
        session['file-upload'] = f'/static/profile_images/{filename}'

        flash('Profile picture updated successfully!')
    else:
        flash('No file selected. Please choose a file.')

    return redirect(url_for('profile'))



        
def search():
    search_query = request.args.get('query', '').lower()  # Get the search query from the user

    # Search for matching alt texts
    matching_pages = [page for page in pages if search_query in page['alt_text'].lower()]
    
    return render_template('search_results.html', matching_pages=matching_pages)



@app.route('/homepage', methods=['GET', "POST"])
def homepage():
        return render_template('homepage.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/hotels')
def hotels():
    return render_template('hotels.html')


@app.route('/share')
def share():
    return render_template('share.html')


@app.route('/retro')
def retro():
    return render_template('retro.html')

@app.route('/invest')
def invest():
    return render_template('invest.html')

@app.route('/banks')
def banks():
    return render_template('banks.html')

@app.route('/fitness')
def fitness():
    return render_template('fitness.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/internet')
def internet():
    return render_template('internet.html')

@app.route('/submit')
def submit():
    return render_template('submit.html')

@app.route('/health')
def health():
    return render_template('health.html')


@app.route('/submitted', methods=['GET', 'POST'])
def submitted():
    if request.method=='POST':
        website=request.form['website-url']
        img=request.form['img-url']        
        email=session['email']
        username=session['username']
        subject="Website Submission",  # email subject

        if not email:
            flash("No email in session", 'danger')
            return redirect(url_for('signInPage'))
        
        user_message = Message(
            subject="Thank You for Your Website Submission",  # Email subject
            sender=app.config['MAIL_USERNAME'],  # Sender email (your email)
            recipients=[email]  # Recipient email (user's email from session)
        )
        
        # Setting the body of the email
        user_message.body = f"Hi {username},\n\nThank you for submitting the website: {website}.\n\n" \
                            f"We have received the following details:\n" \
                            f"Website: {website}\n" \
                            f"Image URL: {img}\n\n" \
                            f"Your submission will be added shortly.\n\n" \
                            f"Best regards,\nRed Rat Games"
        
        # Send the email to the user
        mail.send(user_message)

        message = Message(
            subject=subject,
            sender=app.config['MAIL_USERNAME'],  # sender's email
            recipients=[email]  # recipient's email
        )  # recipient email(s)
        message.body=f"Subject: {subject}\n Image Link: {img}\nEmail: {email}\nUsername: {username}\n Website: {website}"
        mail.send(message)

        flash("Message Sent To My Email!", 'success')
    return redirect(url_for('homepage'))

@app.route('/userCreated', methods=['GET', 'POST'])
def userCreated():
    if request.method=='POST':
        website=request.form['created-website-url']
        img=request.form['created-img-url']        
        email=session['email']
        name=request.form['company-name']
        username=session['username']
        subject="User Created Website",  
        message=request.form['message']# email subject

        if not email:
            flash("No email in session", 'danger')
            return redirect(url_for('signInPage'))
        
        user_message = Message(
            subject="Thank You for Your Website ",  # Email subject
            sender=app.config['MAIL_USERNAME'],  # Sender email (your email)
            recipients=[email]  # Recipient email (user's email from session)
        )
        
        # Setting the body of the email
        user_message.body = f"Hi {username},\n\nThank you for submitting your website: {website}.\n\n" \
                            f"We have received the following details:\n" \
                            f"Website: {website}\n" \
                            f"Image URL: {img}\n" \
                            f"Name: {name}\n"\
                            f"Message: {message}\n\n"\
                            f"Your submission will be added shortly.\n\n" \
                            f"Best regards,\nRed Rat Games"
        
        # Send the email to the user
        mail.send(user_message)

        message = Message(
            subject=subject,
            sender=app.config['MAIL_USERNAME'],  # sender's email
            recipients=[email]  # recipient's email
        )  # recipient email(s)
        message.body=f"Subject: {subject}\n Image Link: {img}\nEmail: {email}\nUsername: {username}\nname: {name}\n Website:  {website}\nMessage {message}"
        mail.send(message)

        flash("Message Sent To My Email!", 'success')
    return redirect(url_for('homepage'))

@app.route('/ottoojala')
def otto():
    return render_template('otto.html')

@app.route('/socialmedia')
def socialMedia():
    return render_template('socials.html')

@app.route('/neilsgames')
def neilsgames():
    return render_template('neilsGames.html')

@app.route('/profile', methods=['GET'])
def profile():
    if 'username' not in session:
        flash('You need to sign in first.')
        return redirect(url_for('signInPage'))

    user_id = get_user_id(session['username'])

    try:
        with sqlite3.connect('account.db') as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT url, name FROM user_websites WHERE user_id = ? AND type = "favorite"', (user_id,))
            favorites = cursor.fetchall()

            cursor.execute('SELECT url, name FROM user_websites WHERE user_id = ? AND type = "liked"', (user_id,))
            liked = cursor.fetchall()

        # Debug: Print the values passed to the template
        print(f"Favorites: {favorites}")
        print(f"Liked: {liked}")

        return render_template('profile.html', favorites=favorites, liked=liked)

    except Exception as e:
        flash(f'Error loading profile: {e}')
        return render_template('signInPage.html')


@app.route('/work')
def work():
    return render_template('work.html')

@app.route('/workspace')
def workspace():
    return render_template('workspace.html')

@app.route('/office')
def office():
    return render_template('office.html')


@app.route('/personal')
def personal():
    return render_template('personal.html')

@app.route('/doublespeak')
def doublespeak():
    return render_template('doublespeak.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/financial')
def financial():
    return render_template('financial.html')

@app.route('/ai')
def ai():
    return render_template('ai.html')

@app.route('/credit')
def credit():
    return render_template('credit.html')

@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/insurance')
def insurance():
    return render_template('insurance.html')

@app.route('/groceries')
def groceries():
    return render_template('groceries.html')

@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')

@app.route('/mind')
def mind():
    return render_template('mind.html')

@app.route('/supply')
def supply():
    return render_template('supply.html')

@app.route('/currency')
def currency():
    return render_template('currency.html')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

@app.route('/art')
def art():
    return render_template('art.html')

@app.route('/money')
def money():
    return render_template('money.html')

@app.route('/artists')
def artists():
    return render_template('artists.html')

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/gambling')
def gambling():
    return render_template('gambling.html')



@app.route('/designers')
def designers():
    return render_template('designers.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/developers')
def developers():
    return render_template('developers.html')


@app.route('/elephantcollection')
def elephantcollection():
    return render_template('elephantcollection.html')

@app.route('/henrystickmincollection')
def henrystickmancollection():
    return render_template('henry.html')

@app.route('/google')
def google():
    return render_template('google.html')

@app.route('/innogames')
def innogames():
    return render_template('inno.html')

@app.route('/iogames')
def iogames():
    return render_template('io.html')

@app.route('/juicygames')
def juicygames():
    return render_template('juicy.html')

@app.route('/multiplayer')
def multiplayer():
    return render_template('multiplayer.html')

@app.route('/newgrounds')
def newgrounds():
    return render_template('newgrounds.html')

@app.route('/newyorktimes')
def newyorktimes():
    return render_template('nyt.html')

@app.route('/online')
def online():
    return render_template('online.html')

@app.route('/orteil')
def orteil():
    return render_template('orteil.html')

@app.route('/phoboslab')
def phoboslab():
    return render_template('phoboslab.html')

@app.route('/popular')
def popular():
    return render_template('popular.html')

@app.route('/wix')
def wix():
    return render_template('wix.html')

@app.route('/otherwebsites')
def otherwebsites():
    return render_template('Fun.html')

@app.route('/recomendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/clear_all_websites', methods=['POST'])
def clear_all_websites():
    if 'username' not in session:
        return render_template('signInPage.html')

    user_id = get_user_id(session['username'])  # Helper function to get user ID

    try:
        with sqlite3.connect('account.db') as conn:
            cursor = conn.cursor()
            # Delete all favorite and liked websites for the user
            cursor.execute('''
                DELETE FROM user_websites WHERE user_id = ?
            ''', (user_id,))
            conn.commit()

        flash({'success': True, 'message': 'All websites cleared successfully.'})
        return render_template('profile.html')
    except Exception as e:
        flash({'success': False, 'message': str(e)}), 500
        return render_template('signInPage.html')


@app.route('/clothing')
def clothing():
    return render_template('clothing.html')

@app.route('/shopping')
def shopping():
    return render_template('shopping.html')

@app.route('/timeline')
def timeline():
    return render_template('Timeline.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/media')
def media():
    return render_template('media.html')

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/retail')
def retail():
    return render_template('retail.html')

@app.route('/electronics')
def electronics():
    return render_template('electronics.html')

@app.route('/social')
def social():
    return render_template('social.html')

@app.route('/luxury')
def luxury():
    return render_template('luxury.html')

@app.route('/books')
def reading():
    return render_template('reading.html')


@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/collections')
def collections():
    return render_template('collections.html')

@app.route('/entertainment')
def entertainment():
    return render_template('entertainment.html')

@app.route('/business')
def business():
    return render_template('business.html')

@app.route('/math')
def math():
    return render_template('math.html')

@app.route('/shows')
def shows():
    return render_template('shows.html')

@app.route('/encyclopedias')
def encyclopedia():
    return render_template('encyclopedia.html')

@app.route('/news')
def news():
    return render_template('news.html')



@app.route('/donate', methods=['GET', "POST"] )
def donate():
    return render_template('donate.html')

@app.route('/originalgames')
def originalgames():
    return render_template('original.html')



if __name__ == "__main__":
    socketio.run(app, debug=True)
  # Initialize the database


    


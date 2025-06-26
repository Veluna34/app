from flask import Flask, redirect, url_for, render_template, request, session, flash, render_template_string, jsonify
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
import requests
from transformers import pipeline
import re



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
    'online.html',
    'newgrounds.html',
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
    'users.html',
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
    'groceries.html',
    'events.html'
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
    'projects.html':'Crafts & Rennovations (Work)',
    'reading.html':'Stream Your Books (Entertainment)',
    'recommendations.html':'Games I Recommend',
    'retail.html':'Retail Stores (Shopping)',
    'retro.html':'Retro Games (Games)',
    'shows.html':'Stream Your Shows (Media)',
    'Timeline.html':'The Timeline (Games)',
    'users.html':'Independant Web Devlopers',
    'video.html':'For Video Editing (Design)',
    'workspace.html': 'Googe Workspace (Productivity)',
    'homepage.html': 'The Red Rat Web',
    'users.html':'User Submitted Websites (Community)',
    'insurance.html': 'Insurance Services (Fincances)',
    'invest.html': 'Invest Your Money (Finances)',
    'banks.html': 'Online Banking (Finances)',
    'currency.html': 'Online Currencies (Finances)',
    'gambling.html': 'Gambling & Betting (Finances)',
    'credit.html': 'Credit Card Services (Finances)',
    'financial.html': 'General Financial Tools (Finances)',
    'delivery.html': 'Delivery/Transportation Services',
    'supply.html': 'Supplies For Home & DIY Projects (Shopping)',
    'marketplace.html': 'Marketplaces (Shopping)',
    'internet.html': 'Internet Services',
    'fitness.html': 'Workout & Weight Programs (Health)',
    'mind.html': 'Mental Health (Health)',
    'hotels.html': 'Hotels & Housing (Travel)',
    'travelling.html': 'Flight Services (Travel)',
    'events.html': 'Events & Tickets (Shopping)',
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

nlp_model = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-3")

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

@app.route("/test")
def test():
    return render_template('test.html')


# Define a list of websites to crawl
nlp_model = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')


websites_by_category = {
    "art": [
        "https://www.blender.org",  # 3D art and animation
        "https://www.artstation.com",  # Digital art portfolio
        "https://www.cgtrader.com",  # 3D models marketplace
        "https://www.turbosquid.com",  # 3D assets
        "https://www.deviantart.com",  # Art sharing platform
        "https://www.behance.net",  # Creative portfolio
        "https://www.pixiv.net"  # Japanese art and illustration sharing
    ],
    "business": [
        "https://www.forbes.com",  # Business news
        "https://www.inc.com",  # Small business advice
        "https://www.businessinsider.com",  # News and trends
        "https://www.entrepreneur.com",  # Resources for entrepreneurs
        "https://www.mckinsey.com",  # Consulting and business insights
        "https://www.hbr.org",  # Harvard Business Review
        "https://www.fastcompany.com"  # Business and innovation news
    ],
    "technology": [
        "https://www.techcrunch.com",  # Tech industry news
        "https://www.wired.com",  # Technology and science
        "https://www.theverge.com",  # Tech, science, and culture
        "https://www.arstechnica.com",  # Technology-focused news
        "https://www.gizmodo.com",  # Technology and gadget news
        "https://www.tomshardware.com",  # PC and hardware
        "https://www.howtogeek.com"  # Tech tutorials and guides
    ],
    "education": [
        "https://www.khanacademy.org",  # Free educational content
        "https://www.coursera.org",  # Online courses
        "https://www.edx.org",  # Online university-level courses
        "https://www.udemy.com",  # Learn anything from courses
        "https://www.ted.com",  # Educational and inspirational talks
        "https://www.openculture.com",  # Free cultural and educational media
        "https://www.academia.edu"  # Research papers and academic content
    ],
    "health": [
        "https://www.webmd.com",  # Medical information
        "https://www.mayoclinic.org",  # Health advice
        "https://www.healthline.com",  # Health and wellness
        "https://www.cdc.gov",  # Public health info
        "https://www.nih.gov",  # Medical research
        "https://www.who.int",  # World Health Organization
        "https://www.medicalnewstoday.com"  # Health news and articles
    ],
    "science": [
        "https://www.sciencemag.org",  # Science news
        "https://www.nature.com",  # Scientific journals
        "https://www.space.com",  # Space and astronomy
        "https://www.scientificamerican.com",  # Science and technology
        "https://www.nasa.gov",  # NASA space-related content
        "https://www.phys.org",  # Physics and general science
        "https://www.livescience.com"  # Science news and explanations
    ],
    "finance": [
        "https://www.bloomberg.com",  # Financial news
        "https://www.wsj.com",  # Wall Street Journal
        "https://www.marketwatch.com",  # Market insights
        "https://www.investopedia.com",  # Investment education
        "https://www.nerdwallet.com",  # Personal finance tips
        "https://www.morningstar.com",  # Investment research
        "https://www.robinhood.com"  # Stock trading
    ],
    "gaming": [
        "https://www.ign.com",  # Video game reviews and news
        "https://www.gamespot.com",  # Game-related news
        "https://www.pcgamer.com",  # PC gaming
        "https://www.kotaku.com",  # Gaming culture and news
        "https://www.twitch.tv",  # Game streaming
        "https://www.rockpapershotgun.com",  # PC gaming news
        "https://www.metacritic.com/game"  # Game reviews aggregator
    ],
    "travel": [
        "https://www.tripadvisor.com",  # Travel reviews
        "https://www.expedia.com",  # Travel booking
        "https://www.airbnb.com",  # Short-term accommodations
        "https://www.lonelyplanet.com",  # Travel guides
        "https://www.booking.com",  # Hotel bookings
        "https://www.skyscanner.net",  # Flights and hotels
        "https://www.kayak.com"  # Travel deals
    ],
    "news": [
        "https://www.bbc.com",  # Global news
        "https://www.cnn.com",  # U.S. and global news
        "https://www.nytimes.com",  # News and analysis
        "https://www.reuters.com",  # International news
        "https://www.aljazeera.com",  # News and current events
        "https://www.theguardian.com",  # News and opinion
        "https://www.apnews.com"  # Associated Press
    ],
    "sports": [
        "https://www.espn.com",  # Sports news and scores
        "https://www.nfl.com",  # NFL updates
        "https://www.nba.com",  # NBA updates
        "https://www.mlb.com",  # MLB updates
        "https://www.skysports.com",  # Sports news and analysis
        "https://www.fifa.com",  # Soccer and FIFA
        "https://www.olympic.org"  # Olympic Games
    ],
    "shopping": [
        "https://www.amazon.com",  # Online shopping
        "https://www.ebay.com",  # Auctions and shopping
        "https://www.walmart.com",  # General retail
        "https://www.target.com",  # Retail shopping
        "https://www.bestbuy.com",  # Electronics shopping
        "https://www.etsy.com",  # Handmade and unique goods
        "https://www.alibaba.com"  # Wholesale products
    ],
    "programming": [
        "https://www.github.com",  # Code hosting
        "https://www.stackoverflow.com",  # Coding questions and answers
        "https://www.codewars.com",  # Coding challenges
        "https://www.freecodecamp.org",  # Free coding tutorials
        "https://www.hackerrank.com",  # Coding practice
        "https://www.gitlab.com",  # Git repository hosting
        "https://www.replit.com"  # Online IDE and coding platform
    ],
    "movies": [
        "https://www.imdb.com",  # Movies and TV database
        "https://www.rottentomatoes.com",  # Movie reviews
        "https://www.metacritic.com/movie",  # Movie scores
        "https://www.netflix.com",  # Streaming movies
        "https://www.hulu.com",  # TV shows and movies
        "https://www.disneyplus.com",  # Disney movies and shows
        "https://www.criterion.com"  # Classic films
    ],

        "movie": [
        "https://www.imdb.com",  # Movies and TV database
        "https://www.rottentomatoes.com",  # Movie reviews
        "https://www.metacritic.com/movie",  # Movie scores
        "https://www.netflix.com",  # Streaming movies
        "https://www.hulu.com",  # TV shows and movies
        "https://www.disneyplus.com",  # Disney movies and shows
        "https://www.criterion.com"  # Classic films
    ],

    "food": [
        "https://www.allrecipes.com",  # Recipes and cooking tips
        "https://www.foodnetwork.com",  # Cooking shows and recipes
        "https://www.epicurious.com",  # Food and drink recipes
        "https://www.yummly.com",  # Recipe recommendations
        "https://www.tasty.co",  # Video recipes
        "https://www.bonappetit.com",  # Food news and recipes
        "https://www.seriouseats.com"  # In-depth cooking guides
    ],

    "music": [
        "https://www.spotify.com", 
        "https://www.apple.com/music", 
        "https://www.soundcloud.com", 
        "https://www.bandcamp.com", 
        "https://www.pandora.com", 
        "https://www.tidal.com", 
        "https://www.audible.com"
    ],

    "fashion": [
        "https://www.vogue.com", 
        "https://www.hm.com", 
        "https://www.zara.com", 
        "https://www.asos.com", 
        "https://www.farfetch.com", 
        "https://www.ssense.com", 
        "https://www.shein.com"
    ],

    "books": [
        "https://www.goodreads.com", 
        "https://www.audible.com", 
        "https://www.scribd.com", 
        "https://www.projectgutenberg.org", 
        "https://www.librivox.org", 
        "https://www.bookdepository.com", 
        "https://www.powells.com"
    ],
    "fitness": [
        "https://www.bodybuilding.com", 
        "https://www.myfitnesspal.com", 
        "https://www.fitnessblender.com", 
        "https://www.nerdfitness.com", 
        "https://www.mapmyrun.com", 
        "https://www.strava.com", 
        "https://www.acefitness.org"
    ],

        "history": [
        "https://www.history.com",  # History documentaries and articles
        "https://www.archives.gov",  # U.S. National Archives
        "https://www.britannica.com",  # Encyclopedic history resource
        "https://www.livescience.com/history",  # History and archaeology
        "https://www.smithsonianmag.com/history",  # Smithsonian historical articles
        "https://www.nationalarchives.gov.uk",  # UK National Archives
        "https://www.historyextra.com"  # History magazine
    ],
    "automotive": [
        "https://www.autoblog.com",  # Automotive news
        "https://www.motortrend.com",  # Car reviews and automotive news
        "https://www.caranddriver.com",  # Vehicle reviews and specs
        "https://www.edmunds.com",  # Car buying advice
        "https://www.autotrader.com",  # Vehicle marketplace
        "https://www.kbb.com",  # Car value and reviews
        "https://www.roadandtrack.com"  # Automotive culture and reviews
    ],
    "environment": [
        "https://www.nationalgeographic.com",  # Environment and nature news
        "https://www.treehugger.com",  # Sustainability and environmental news
        "https://www.greenpeace.org",  # Environmental advocacy
        "https://www.sierraclub.org",  # Environmental organization
        "https://www.earthwatch.org",  # Environmental conservation projects
        "https://www.earthday.org",  # Environmental protection
        "https://www.wwf.org"  # World Wildlife Fund
    ],
        "nature": [
        "https://www.nationalgeographic.com",  # Nature documentaries and articles
        "https://www.worldwildlife.org",  # Wildlife conservation and nature preservation
        "https://www.mountainsmith.com",  # Outdoor adventure gear and tips
        "https://www.nature.org",  # Environmental conservation and sustainability
        "https://www.thenatureconservancy.org",  # Nature preservation and eco-tourism
        "https://www.greenpeace.org",  # Global environmental activism
        "https://www.wilderness.org"  # Protecting America's wild places
    ],

        "mental": [
        "https://www.psychologytoday.com",  # Articles on mental health and therapy resources
        "https://www.headspace.com",  # Meditation and mindfulness exercises
        "https://www.talkspace.com",  # Online therapy services
        "https://www.mhanational.org",  # Mental Health America advocacy and resources
        "https://www.betterhelp.com",  # Online counseling and therapy
        "https://www.nami.org",  # National Alliance on Mental Illness
        "https://www.suicidepreventionlifeline.org"  # Suicide prevention resources and hotline
    ],

       "professionalMedia": [
        "https://www.linkedin.com",  # Professional networking platform
        "https://www.twitter.com",  # Social network with a professional side
        "https://www.xing.com",  # European professional networking site
        "https://www.meetup.com",  # Event hosting and networking
        "https://www.clubhouse.com",  # Audio-based social network for professionals
        "https://www.glassdoor.com",  # Reviews of companies and job listings
        "https://www.reddit.com/r/entrepreneur"  # Entrepreneur-focused subreddit
    ],

       "personalMedia": [
        "https://www.facebook.com",  # General social networking
        "https://www.instagram.com",  # Photo and video sharing
        "https://www.snapchat.com",  # Multimedia messaging
        "https://www.twitter.com",  # Microblogging and social networking
        "https://www.tiktok.com",  # Short video sharing platform
        "https://www.pinterest.com",  # Image sharing and discovery
        "https://www.whatsapp.com"  # Instant messaging and voice calls
    ],

    "video": [
    "https://www.youtube.com",  # Video sharing and creation platform
    "https://www.twitch.tv",  # Live streaming and video gaming
    "https://www.vimeo.com",  # Video hosting and sharing platform
    "https://www.bandicam.com",  # Screen recording and video capture
    "https://www.dailymotion.com",  # Video hosting and sharing
    "https://www.obspproject.com",  # Open-source streaming and recording software
    "https://www.streamlabs.com"  # Live streaming and broadcasting tools
    ],

    "manage": [
        "https://www.asana.com",  # Task and project management
        "https://www.trello.com",  # Visual project management and collaboration
        "https://www.slack.com",  # Team communication and collaboration
        "https://www.monday.com",  # Work management and team collaboration
        "https://www.basecamp.com",  # Project management and team collaboration
        "https://www.quickbooks.intuit.com",  # Accounting and financial management
        "https://www.salesforce.com"  # Customer relationship management (CRM)
    ],

    "internet": [
    "https://www.xfinity.com",  # Comcast's internet service
    "https://www.att.com",  # AT&T internet services
    "https://www.verizon.com",  # Verizon internet service
    "https://www.spectrum.com",  # Spectrum internet service
    "https://www.frontier.com",  # Frontier internet service
    "https://www.cox.com",  # Cox internet service
    "https://www.optimum.com"  # Optimum internet service
    ],

        "gaming": [
    "https://store.steampowered.com/",  # Comcast's internet service
    "https://www.g2a.com/?adid=GA-US_PB_MIX_SN_PURE_BRAND-English&id=35&utm_medium=cpc&utm_source=google&utm_campaign=GA-US_PB_MIX_SN_PURE_BRAND-English&utm_id=18956348617&gad_source=1&gclid=Cj0KCQiAv628BhC2ARIsAIJIiK8gxWJGFNN4lJLyIasuHJe4YHvBXEqX36fx9n2zZsFsiXN4N0SaYYMaAjiTEALw_wcB&gclsrc=aw.ds",  # AT&T internet services
    "https://store.epicgames.com/en-US/",  # Verizon internet service
    "https://www.playstation.com/en-us/",  # Spectrum internet service
    "https://www.xbox.com/en-US/microsoft-store",  # Frontier internet service
    "https://www.nintendo.com/us/",  # Cox internet service
    "https://www.dell.com/en-us/gaming/alienware"  # Optimum internet service
    ],
            "electronics": [
    "https://www.samsung.com/us/smartphones/the-next-galaxy/reserve/?cid=sem-mktg-pfs-mob-us-google-na-01062025-142549-&ds_e=GOOGLE-cr:0-pl:382719933-&ds_c=CN~Samsung-Core_ID~n_PR~f1h24-e1_SB~smart_PH~long_KS~ba_MK~us_OB~conv_FS~lo_FF~n_BS~mx_KM~exact-&ds_ag=ID~n_AG~Samsung+Core_AE~mass_AT~stads_MD~h_PK~roah_PB~google_PL~sa360_CH~search_FF~Mass+Target-&ds_k=samsung&gad_source=1&gclid=Cj0KCQiAv628BhC2ARIsAIJIiK8KTRHI_pzp9gTxIdgZ3wEB5k5Oe2V-HK0uRVJWI_1LHdiSZd8EascaAt8-EALw_wcB&gclsrc=aw.ds",  # Comcast's internet service
    "https://www.apple.com/store?afid=p238%7CseIEs444j-dc_mtid_1870765e38482_pcrid_724099485023_pgrid_13945964887_pntwk_g_pchan__pexid__ptid_kwd-10778630_&cid=aos-us-kwgo-brand-apple--slid---product-",  # AT&T internet services
    "https://www.asus.com/us/laptops/for-home/all-series/asus-zenbook-a14-ux3407/?utm_source=google&utm_medium=cpc&utm_campaign=25q1_ces_hq&utm_content=sem&gad_source=1&gclid=Cj0KCQiAv628BhC2ARIsAIJIiK84Rg1Y97pSYHy21aLwQ0VDgZBAu4ujJon1Iq5SACo6am3HL4aYHwcaAgJVEALw_wcB",  # Verizon internet service
    "https://www.acer.com/us-en",  # Spectrum internet service
    "https://www.arduino.cc/",  # Frontier internet service
    "https://www.raspberrypi.com/",  # Cox internet service
    "https://www.lego.com/en-us/themes/mindstorms?consent-modal=show"  # Optimum internet service
    ]
}

def crawl_website(url):
    """Crawl a given website and extract textual content."""
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        paragraphs = soup.find_all('p')
        page_text = ' '.join([para.text for para in paragraphs if para.text.strip() != ''])
        return page_text
    except Exception as e:
        print(f"Failed to crawl {url}: {str(e)}")
        return ""

def analyze_relevance(prompt, websites_by_category):
    """Analyze the relevance of the scraped websites based on the user prompt."""
    relevance_scores = []
    
    # Normalize the prompt to lowercase to handle case insensitivity
    prompt = prompt.lower()

    # Find the relevant category based on the prompt
    selected_category = None
    for category in websites_by_category:
        if category in prompt:  # Match category by keyword
            selected_category = category
            break

    if not selected_category:
        return {"error": "No relevant category found for your prompt"}

    # Get the websites that belong to the selected category
    websites = websites_by_category[selected_category]

    # Loop through all the websites and get the relevance score for each
    for website in websites:
        page_text = crawl_website(website)
        
        if page_text:  # Only analyze if text was successfully scraped
            # Perform zero-shot classification to evaluate relevance to the prompt
            result = nlp_model(prompt, candidate_labels=[selected_category])
            
            # Store the relevance score and website URL
            relevance_scores.append((website, result['scores'][0]))  # Score of relevance
    
    # Sort the websites based on the highest relevance score
    relevance_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return the top 4 most relevant websites
    return [website for website, score in relevance_scores[:7]]

@app.route('/get_relevant_links', methods=['POST'])
def get_relevant_links():
    data = request.get_json()
    user_input = data.get('prompt')

    if not user_input:
        return jsonify({"error": "No category provided"}), 400

    # Normalize user input to lowercase for case-insensitive matching
    user_input_lower = user_input.lower()

    # Bold the category keywords in the user input
    for category in websites_by_category:
        # Check if the category is in the input string (case-insensitive)
        if category.lower() in user_input_lower:
            # Use re.sub to replace and add the <b> tags with case insensitivity
            bold_category = f"<b>{category}</b>"
            # Replace all occurrences of the category in the user input (case-insensitive)
            user_input = re.sub(re.escape(category), bold_category, user_input, flags=re.IGNORECASE)

    # Find the relevant category by checking for partial matches
    selected_category = None
    for category in websites_by_category:
        if category.lower() in user_input_lower:  # Check if the input word is part of a category
            selected_category = category
            break

    if not selected_category:
        return jsonify({"error": f"No relevant category found for your input: '{user_input}'"}), 400

    # Get the websites that belong to the selected category
    relevant_links = websites_by_category.get(selected_category, [])

    if not relevant_links:
        return jsonify({"error": f"No websites found for category '{selected_category}'"}), 400

    # Return the modified user input with bolded category words along with the relevant links
    return jsonify({
        "modified_prompt": user_input,  # Modified prompt with bolded category names
        "links": relevant_links
    })




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
        'ai.html': ['Artificial Intelligence', 'A.I.', 'ai', 'A.I. Tools', 'ai tools', 'tools', 'working', 'productivity', 'effeciency', 'business'],
        'art.html': ['art', 'deign', 'art tools', 'working', 'art deign', 'work', 'tools', 'media'],
        'artists.html': ['art', 'deign', 'art tools', 'working', 'art deign', 'media'],
        'artists.html': ['music', 'music production', 'music design', 'working', 'dsign tools', 'tools', 'media'],
        'business.html': ['general', 'productivity','working', 'effeciancy', 'business'],
        'clothing.html': ['clothes', 'clothing','online shops', 'online shopping', 'online stores'],
        'collections.html': ['game collections', 'browser games','entertainment' 'media'],
        'designers.html': ['tools', 'general design','working', 'business'],
        'developers.html': ['developers', 'coding','code', 'programming', 'programs', 'work', 'tools', 'design', 'business'],
        'doublespeak.html': ['doublespeak games', 'browser games','entertainment', 'media'],
        'electronics.html': ['electronics', 'online shops','online shopping', 'devices'],
        'elephantCollection.html': ['browser games', 'Elephant collection','entertainment','media'],
        'encyclopedia.html': ['information', 'encyclopedias','work', 'tools', 'research'],
        'entertainment.html': ['entertainment', 'online shops','online shopping', 'games', 'media', 'books', 'music', 'comics', 'media'],
        'Fun.html': ['other Websites', 'fun','games', 'reccomendations'],
        'google.html': ['browser games', 'google','entertainment', 'media'],
        'henry.html': ['henry stickmin collection', 'entertainment','browser games', 'media'],
        'inno.html': ['Inno Games', 'Browser Games','entertainment', 'media'],
        'i0.html': ['Popular IO Games', 'Browser Games','entertainment', 'media'],
        'juicy.html': ['Juicy Games', 'Browser Games','entertainment', 'media'],
        'luxury.html': ['Luxury Stores', 'High end stores','online shopping', 'online shops', 'clothes', 'clothing'],
        'math.html': ['Math', 'science','tools', 'work', 'math tools', 'science tools', 'calculators', 'graphing', 'productivity'],
        'multiplayer.html': ['popular coop games', 'popular multiplayer games','browser games', 'entertainment', 'media'],
        'music.html': ['music', 'streaming','podcasts', 'entertainment', 'media'],
        'neilsGames.html': ['Neil.fun', 'Browser Games','entertainment', 'media'],
        'newgorunds.html': ['popualar games from Newgrounds', 'Browser games','entertainment', 'media'],
        'news.html': ['information', 'news','entertainment', 'media', 'research', 'business'],
        'nyt.html': ['games from the new york times','entertainment', 'media', 'browser games'],
        'office.html': ['microsoft office','work', 'tools', 'productivity'],
        'online.html': ['popular online games','browser games', 'media', 'entertainment'],
        'original.html': ['original games','browser games', 'media', 'entertainment', 'the red rat web'],
        'orteil.html': ['games from orteil','browser games', 'media', 'entertainment', 'orteil games'],
        'otto.html': ['games from otto ojala','browser games', 'media', 'entertainment', 'Otto ojala games'],
        'personal.html': ['personal social media','media', 'entertainment', 'work', 'tools'],
        'phoboslab.html': ['phoboslab games','media', 'entertainment','browser games'],
        'popular.html': ['popular games','media', 'entertainment', 'browser games'],
        'professional.html': ['professional social meda','media', 'entertainment', 'work', 'tools'],
        'professional.html': ['professional social meda','media', 'entertainment', 'work', 'tools'],
        'projects.html': ['projects','online shopping', 'online shops', 'work', 'tools', 'arts and crafts'],
        'reading.html': ['streaming services' ,'books', 'reading', 'information', 'entertainment', 'media'],
        'recommendations.html': ['games i recommend','recommendations', 'games', 'entertainment', 'media'],
        'retail.html': ['retail stores','online shopping', 'online shops', 'retail shops'],
        'retro.html': ['retro games','popular games', 'browser games', 'entertainment', 'media'],
        'shows.html': ['shows','movies', 'videos', 'streaming services', 'streaming platforms', 'media', 'entertainment', 'tv', 't.v.', 'television'],
        'timeline.html': ['videos','music', 'games', 'information', 'research', 'media', 'entertainment', 'The Timeline'],
        'users.html': ['independant developers','websites', 'user cerated websites', 'other websites', 'media', 'math', 'calculus', 'health', 'working out', 'the gym', 'fitness'],
        'video.html': ['video editing','tools', 'videos', 'entertainment', 'media', 'design'],
        'wix.html': ['Wix Games', 'Browser Games', 'entertainment', 'media'],
        'workspace.html': ['Google Workspace', 'office tools', 'work', 'prodcutivity'],
        'users.html': ['user submitted websites', 'community', 'from users', 'people', 'from people'],
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
        'events.html': ['events', 'Shopping', 'tickets', 'live events', 'things to do', 'activities', 'fun', 'entertainment'],
        'groceries.html': ['Grocery Stores', 'Shopping', 'Groceries', 'food', 'supplies', 'health', 'supply', 'resources'],
        'io.html': ['IO Games', 'Online Games.', 'Multiplayer', 'Fun', 'Entertainment']
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
    
@app.route('/add_to_category', methods=['POST'])
def add_to_category():
    # Check if the user is logged in
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'You need to sign in to perform this action.'}), 401

    # Get the user ID from the session
    user_id = get_user_id(session['username'])
    
    # Parse JSON data from the request
    try:
        data = request.get_json()
        website_url = data.get('url')
        website_name = data.get('name')
        category_id = data.get('category_id')
    except Exception as e:
        return jsonify({'success': False, 'message': f'Invalid JSON payload: {str(e)}'}), 400

    # Validate required fields
    if not all([website_url, website_name, category_id]):
        return jsonify({'success': False, 'message': 'All fields (url, name, category_id) are required.'}), 400

    try:
        # Connect to the database
        with sqlite3.connect('account.db') as conn:
            cursor = conn.cursor()

            # Check if the website already exists in the selected category
            cursor.execute('''
                SELECT id FROM user_websites
                WHERE user_id = ? AND category_id = ? AND url = ?
            ''', (user_id, category_id, website_url))
            existing_website = cursor.fetchone()

            if existing_website:
                # If website exists in the category, return an error message
                return jsonify({'success': False, 'message': 'This website already exists in the selected category.'}), 400
            
            # Insert the website into the selected category
            cursor.execute('''
                INSERT INTO user_websites (user_id, url, name, category_id)
                VALUES (?, ?, ?, ?)
            ''', (user_id, website_url, website_name, category_id))
            conn.commit()

        # Return success response
        return jsonify({'success': True, 'message': 'Website added to category successfully.'}), 201
    except sqlite3.Error as e:
        # Handle database errors
        return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({'success': False, 'message': f'An unexpected error occurred: {str(e)}'}), 500




    
@app.route('/create_category', methods=['POST'])
def create_category():
    if 'username' not in session:
        flash('You need to sign in to perform this action.', 'error')
        return redirect(url_for('signInPage'))

    user_id = get_user_id(session['username'])
    category_name = request.json.get('name')

    if not category_name:
        return {'success': False, 'message': 'Category name is required.'}, 400

    try:
        with sqlite3.connect('account.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO categories (user_id, name) VALUES (?, ?)', (user_id, category_name))
            conn.commit()
        return {'success': True, 'message': 'Category created successfully.'}
    except Exception as e:
        return {'success': False, 'message': str(e)}, 500
    
def delete_category_from_database(category_id):
    # Replace with your database logic
    try:
        # Example: db.session.delete(Category.query.get(category_id))
        return True
    except Exception as e:
        print(f"Error deleting category: {e}")
        return False
    
def delete_website_from_database(url):
    try:
        # Assuming a database connection is available as `conn`
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()

        # Deleting the website from the user_websites table
        cursor.execute("DELETE FROM user_websites WHERE url = ?", (url,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting website: {e}")
        return False

    
@app.route('/delete_website', methods=['POST'])
def delete_website():
    data = request.get_json()
    url = data.get('url')

    # Perform the logic to delete the website from the database
    success = delete_website_from_database(url)

    if success:
        return jsonify(success=True, message="Website deleted successfully.")
    else:
        return jsonify(success=False, message="Failed to delete the website.")
    
@app.route('/delete_category', methods=['POST'])
def delete_category():
    data = request.get_json()
    category_id = data.get('id')

    # Perform the logic to delete the category from the database
    success = delete_category_from_database(category_id)

    if success:
        return jsonify(success=True, message="Category deleted successfully.")
    else:
        return jsonify(success=False, message="Failed to delete the category.")

def delete_category_from_database(category_id):
    try:
        # Assuming a database connection is available as `conn`
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()

        # Deleting the websites associated with the category
        cursor.execute("DELETE FROM user_websites WHERE category_id = ?", (category_id,))

        # Deleting the category itself
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting category: {e}")
        return False




    
@app.route('/get_categories', methods=['GET'])
def get_categories():
    if 'username' not in session:
        flash('You need to sign in to perform this action.', 'error')
        return redirect(url_for('signInPage'))

    user_id = get_user_id(session['username'])

    try:
        with sqlite3.connect('account.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM categories WHERE user_id = ?', (user_id,))
            categories = cursor.fetchall()

            categories_with_websites = []
            for category in categories:
                cursor.execute('SELECT url, name FROM user_websites WHERE user_id = ? AND category_id = ?', (user_id, category[0]))
                websites = cursor.fetchall()
                categories_with_websites.append({'id': category[0], 'name': category[1], 'websites': websites})

        return jsonify({'success': True, 'categories': categories_with_websites})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

    
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

@app.route('/clear_all_websites', methods=['POST'])
def clear_all_websites():
    if 'username' not in session:
        flash('You need to sign in to perform this action.', 'error')
        return redirect(url_for('signInPage'))

    user_id = get_user_id(session['username'])

    try:
        with sqlite3.connect('account.db') as conn:
            cursor = conn.cursor()

            # Delete all websites from liked/favorites and categories for the user
            cursor.execute('''
                DELETE FROM user_websites
                WHERE user_id = ?
            ''', (user_id,))

            # Delete all categories for the user
            cursor.execute('''
                DELETE FROM categories
                WHERE user_id = ?
            ''', (user_id,))

            conn.commit()

        return {'success': True, 'message': 'All websites and categories cleared successfully.'}
    except Exception as e:
        return {'success': False, 'message': str(e)}, 500


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

@app.route('/events')
def events():
    return render_template('events.html')

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

@app.route('/travel')
def travel():
    return render_template('travel.html')

@app.route('/travelling')
def travelling():
    return render_template('travelling.html')


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

            # Fetch favorite and liked websites
            cursor.execute('SELECT url, name FROM user_websites WHERE user_id = ? AND type = ?', (user_id, 'favorite'))
            favorites = cursor.fetchall()

            cursor.execute('SELECT url, name FROM user_websites WHERE user_id = ? AND type = ?', (user_id, 'liked'))
            liked = cursor.fetchall()

            # Fetch categories and their associated websites in a single query
            cursor.execute('''
                SELECT 
                    c.id AS category_id, 
                    c.name AS category_name, 
                    w.url AS website_url, 
                    w.name AS website_name
                FROM 
                    categories c
                LEFT JOIN 
                    user_websites w 
                ON 
                    c.id = w.category_id AND w.user_id = ?
                WHERE 
                    c.user_id = ?
            ''', (user_id, user_id))
            results = cursor.fetchall()

            # Organize data into a structured dictionary
            categories_with_websites = {}
            for category_id, category_name, website_url, website_name in results:
                if category_id not in categories_with_websites:
                    categories_with_websites[category_id] = {
                        'id': category_id,
                        'name': category_name,
                        'websites': []
                    }
                if website_url and website_name:
                    categories_with_websites[category_id]['websites'].append({
                        'url': website_url,
                        'name': website_name
                    })

        # Convert dictionary to a list for easier template rendering
        categories_with_websites_list = list(categories_with_websites.values())

        # Debug: Print the values passed to the template
        print(f"Favorites: {favorites}")
        print(f"Liked: {liked}")
        print(f"Categories with websites: {categories_with_websites_list}")

        return render_template('profile.html', favorites=favorites, liked=liked, categories_with_websites=categories_with_websites_list)

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

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')


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
    port = int(os.getenv("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)



    


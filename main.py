import discord
from discord.ext import tasks, commands
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


CHANNEL_ID = 69

intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents)

# Function to scrape the movie titles using Selenium
def get_movie_titles():
    options = Options()
    options.add_argument("--headless")


    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the cinema website
    driver.get('https://tickets.talosplaza.gr/#/welcome')

    # Wait for the page to load (adjust timing as necessary)
    time.sleep(5)

    # Scrape movie titles (adjust the selector based on the website)
    movie_elements = driver.find_elements(By.CSS_SELECTOR ,'.spectacle-title')  # Replace with actual selector
    movie_titles = [movie.text for movie in movie_elements]

    # Quit the driver
    driver.quit()

    return movie_titles

# This task will send new movie titles to a Discord channel every 30 minutes
@tasks.loop(minutes=30)
async def send_movie_notifications():
    channel = client.get_channel(CHANNEL_ID)  # Replace with your Discord channel ID

    # Get the latest movie titles by scraping the website
    movie_titles = get_movie_titles()

    # Send the list of movies to the Discord channel
    for title in movie_titles:
        await channel.send(f"New Movie: {title}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    send_movie_notifications.start()  # Start the task to send movie notifications

# Run the bot
client.run('MY-TOKEN')

titles = get_movie_titles()
for t in titles:
    print(t)



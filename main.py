import discord
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()
# Discord bot token
TOKEN = os.environ.get('TOKEN')

# Channel ID of the welcoming channel
WELCOME_CHANNEL_ID = 1079198980442968124

# Font file path for username
FONT_FILE = 'MyriadPro-Light.otf'

# Size of the final image
IMAGE_SIZE = (500, 200)


# Function to generate a custom welcome image
def generate_welcome_image(username, avatar_url):
  # Open the background image and create a new transparent image
  bg = Image.open("background.png").convert("RGBA")
  avatar_img = Image.new('RGBA', bg.size, (255, 255, 255, 0))

  # Get the avatar image and resize it
  response = requests.get(avatar_url)
  avatar = Image.open(BytesIO(response.content))
  avatar = avatar.resize((210, 210))

  # Paste the resized avatar onto the transparent image
  avatar_img.paste(avatar, (61, 61))

  # Create a new image by merging the background image and the avatar image
  result = Image.alpha_composite(avatar_img, bg)
  draw = ImageDraw.Draw(result)
  font = ImageFont.truetype(FONT_FILE, 40)
  draw.text((473, 254), f"{username}", (255, 255, 255), font=font, anchor="ms")
  img_buffer = BytesIO()
  result.save(img_buffer, format="PNG")
  img_buffer.seek(0)
  return img_buffer


# Define the intents your bot needs
intents = discord.Intents.default()
intents.members = True

# Create a Discord client instance with the specified intents
client = discord.Client(intents=intents)


# Event listener for new member joining
@client.event
async def on_member_join(member):
  # Generate the custom welcome image for the new member
  if member.discriminator:
    welcome_image = generate_welcome_image(
      f"{member.name}#{member.discriminator}", member.avatar.url)
  else:
    welcome_image = generate_welcome_image(f"{member.name}", member.avatar.url)

  # Get the welcoming channel
  welcome_channel = client.get_channel(WELCOME_CHANNEL_ID)

  # Send the welcome message with the custom welcome image
  await welcome_channel.send(f'Welcome to the server, {member.mention}!',
                             file=discord.File(welcome_image, 'welcome.png'))


# Run the Discord client
client.run(TOKEN)

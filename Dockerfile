# 1. Start from the official Ollama image
# This gives us a container with Ollama pre-installed.
FROM ollama/ollama:latest

# 2. Install Python 3 and pip
# We need this to run your bot.py script.
RUN apt-get update && apt-get install -y python3 python3-pip

# 3. Set up the working directory inside the container
WORKDIR /app

# 4. Copy and install Python dependencies
# We copy requirements.txt first to take advantage of Docker's caching.
# This step only re-runs if your requirements change.
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. Pre-pull and "warm up" the AI model
# This is the MOST important step for you.
# This "bakes" the model into your Space's image.
# The 'pull' downloads it, and the 'run' loads it once.
# This solves your slow "warm-up" problem!
RUN ollama pull phi3:mini
RUN ollama run phi3:mini "Hello!"

# 6. Copy all your bot's code into the container
COPY bot.py .
COPY ollama_client.py .
COPY usage_manager.py .
COPY usage_data.json .
COPY ollama_manager.py .

# 7. Copy and prepare the startup script
COPY start.sh .
RUN chmod +x /app/start.sh

# 8. Expose the necessary ports
EXPOSE 11434  
EXPOSE 8000   

# 9. Set the final command to run when the Space starts
CMD ["/app/start.sh"]
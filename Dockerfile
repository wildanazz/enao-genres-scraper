FROM python:3.12-slim

WORKDIR /app

COPY . /app

# Install dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    libx11-dev \
    libxrandr2 \
    libxss1 \
    libgdk-pixbuf2.0-0 \
    libdbus-1-3 \
    libxtst6 \
    libatk1.0-0 \
    libnspr4 \
    libnss3 \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libxcomposite1 \
    libxdamage1 \
    libgd3 \
    libdrm2 \
    libgbm1 \
    libvulkan1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (latest stable version)
RUN curl -sS -o google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome.deb \
    && apt-get -y --fix-broken install \
    && rm google-chrome.deb

# Install chromedriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.87/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip -d /app \
    && rm chromedriver-linux64.zip

RUN pip install -r requirements.txt

CMD ["python", "scraper/enao-genre-scraper.py"]
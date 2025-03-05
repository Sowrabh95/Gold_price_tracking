import time
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Selenium setup
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = "https://www.mmtcpamp.com/"

# Data storage for plotting
timestamps = []
prices = []

# Plot setup
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
ax.set_title("Live Gold Price in INR")
ax.set_xlabel("Time")
ax.set_ylabel("Price (₹/gm)")
line, = ax.plot([], [], marker="o", linestyle="-", color="b")

try:
    while True:
        driver.get(url)
        time.sleep(3)  # Allow JavaScript content to load

        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'zOxMd')]/strong/span[3]"))
            )
            gold_price = float(price_element.text.strip())
            timestamp = time.strftime("%H:%M:%S")

            timestamps.append(timestamp)
            prices.append(gold_price)

            # Keep only the last 20 prices for better visualization
            if len(prices) > 20:
                timestamps.pop(0)
                prices.pop(0)

            # Update the plot
            line.set_xdata(range(len(timestamps)))
            line.set_ydata(prices)
            ax.set_xticks(range(len(timestamps)))
            ax.set_xticklabels(timestamps, rotation=45)
            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(0.1)

            print(f"[{timestamp}] Gold Price: ₹{gold_price}/gm")

        except Exception as e:
            print("Error:", str(e))

        time.sleep(10)

except KeyboardInterrupt:
    print("\nScript stopped by user.")
finally:
    driver.quit()
    plt.ioff()
    plt.show()

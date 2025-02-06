from seleniumbase import Driver
import time
import csv

# Initialize the SeleniumBase Driver
driver = Driver(browser="chrome", headless=False)  # Set headless=False to see the browser

# Set to keep track of visited links
visited_links = set()

# CSV file setup
csv_file = "divar_csv2.csv"
csv_columns = [
    "Link", "Area", "Year of Building", "Number of Rooms", "Elevator", "Parking", "Storage",
    "Bale", "Price", "Tabaghe", "Subtitle"
]

# Open the CSV file for writing with UTF-8 encoding
with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=csv_columns)
    writer.writeheader()  # Write the header row

    try:
        # Navigate to the Divar real estate page
        driver.get("https://divar.ir/s/tehran/buy-apartment")
        driver.wait_for_element('a.kt-post-card__action', timeout=100)  # Wait for the listings to load

        while True:
            # Find all listing links on the current page
            listing_links = driver.find_elements('a.kt-post-card__action')

            # Flag to check if any new link was processed in this iteration
            new_link_processed = False

            for link in listing_links:
                # Get the href of the listing
                link_href = link.get_attribute("href")

                # Skip if the link has already been visited
                if link_href in visited_links:
                    continue

                # Add the link to the visited set
                visited_links.add(link_href)

                # Open the listing in a new tab
                driver.execute_script("window.open('');")  # Open a new tab
                driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab
                driver.get(link_href)  # Navigate to the listing

                # Wait for the page to load
                driver.wait_for_element('td.kt-group-row-item--info-row', timeout=10)

                # Scrape the area, year of building, and number of rooms
                info_rows = driver.find_elements('td.kt-group-row-item--info-row')

                # Extract the values with error handling
                area = info_rows[0].text.strip() if len(info_rows) > 0 else "nan"  # Area (e.g., ۵۸)
                year_of_building = info_rows[1].text.strip() if len(info_rows) > 1 else "nan"  # Year of building (e.g., ۱۳۹۵)
                rooms = info_rows[2].text.strip() if len(info_rows) > 2 else "nan"  # Number of rooms (e.g., ۲)

                # Scrape additional information (elevator, parking, storage)
                additional_info = driver.find_elements('td.kt-group-row-item__value.kt-body.kt-body--stable')

                # Extract the values
                elevator = additional_info[0].text.strip() if len(additional_info) > 0 else "nan"  # آسانسور
                parking = additional_info[1].text.strip() if len(additional_info) > 1 else "nan"  # پارکینگ
                storage = additional_info[2].text.strip() if len(additional_info) > 2 else "nan"  # انباری ندارد

                # Scrape the specific elements
                # 1. Check for <p class="kt-unexpandable-row__value">بله</p>
                bale_element = driver.find_elements('p.kt-unexpandable-row__value')
                bale = bale_element[0].text.strip() if len(bale_element) > 0 and bale_element[0].text.strip() == "بله" else "nan"

                # 2. Scrape price
                price_elements = driver.find_elements('p.kt-unexpandable-row__value')
                price = price_elements[1].text.strip() if len(price_elements) > 1 else "nan"  # Price (e.g., ۲٬۹۰۰٬۰۰۰٬۰۰۰ تومان)

                # 3. Scrape tabaghe (floor)
                tabaghe_elements = driver.find_elements('p.kt-unexpandable-row__value')
                tabaghe = tabaghe_elements[3].text.strip() if len(tabaghe_elements) > 3 else "nan"  # Tabaghe (e.g., ۴ از ۴)

                # 4. Scrape the subtitle (time and location)
                subtitle_element = driver.find_elements('div.kt-page-title__subtitle.kt-page-title__subtitle--responsive-sized')
                subtitle = subtitle_element[0].text.strip() if len(subtitle_element) > 0 else "nan"  # Subtitle (e.g., ۳ روز پیش در تهران، جنت‌آباد مرکزی)

                # Prepare the data for CSV
                data = {
                    "Link": link_href,
                    "Area": area,
                    "Year of Building": year_of_building,
                    "Number of Rooms": rooms,
                    "Elevator": elevator,
                    "Parking": parking,
                    "Storage": storage,
                    "Bale": bale,
                    "Price": price,
                    "Tabaghe": tabaghe,
                    "Subtitle": subtitle,
                }

                # Write the data to the CSV file
                writer.writerow(data)

                # Print the scraped data (for debugging)
                print("Scraped:", data)

                # Close the current tab and switch back to the main page
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                # Mark that a new link was processed
                new_link_processed = True

            # If no new links were processed in this iteration, check for the "Show More Listings" button
            if not new_link_processed:
                try:
                    # Find the "Show More Listings" button
                    show_more_button = driver.find_element('button.kt-button.kt-button--primary.kt-button--outlined.post-list__load-more-btn-be092')
                    
                    # Click the button to load more listings
                    show_more_button.click()
                    
                    # Wait for the new listings to load
                    time.sleep(2)
                    
                    # Continue the loop to process the new listings
                    continue
                except:
                    # If the button is not found, break the loop
                    print("No more new listings found.")
                    break

            # Scroll down to load more listings (infinite scrolling)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new listings to load

    finally:
        # Close the browser
        driver.quit()

print(f"Scraping completed. Data saved to {csv_file}.")
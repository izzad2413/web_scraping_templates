# Import the libraries
from playwright.sync_api import Playwright, sync_playwright     # Web automation
import pandas as pd                                             # Data manipulation & storage
import playwright

# creating the web scraping function
def main():
    with sync_playwright() as p:
        page_url = 'your url'
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
        page.goto(page_url, timeout=60000)
        
        scraped_list = []
        
        for page_num in range(1,40):    # define the number of pages to scraped
            print(f"Scraping page {page_num}")

            # locate the rows of the table
            tr = 'xpath'
            
            # locate the data to be extracted
            data_1_path = 'xpath'
            data_2_path = 'xpath'
            data_3_path = 'xpath'
            # continues if any ...

            # to loop each row of the table
            tr_elements = page.query_selector_all(tr)

            # begin looping
            for tr_element in tr_elements:
                
                # Extract data_1: extract text data
                data_1_element = tr_element.query_selector(data_1_path)
                data_1 = data_1_element.inner_text() if data_1_element else '' 

                # Extract data_2: extract data & count them (for extracting integer value)
                data_2_element = tr_element.query_selector_all(data_2_path)
                data_2 = len(data_2_element)
                
                # Extract data_3: extract text data where its being separated by lines
                data_3_element = tr_element.query_selector(data_3_path)
                data_3 = data_3_element.inner_text() if data_3_element else '' 

                # Split hotel_info into lines
                lines = [line.strip() for line in data_3.split('\n')]

                # Extract hotel_name, hotel_address, and hotel_contact
                data_3_1 = lines[0] if lines else ''
                data_3_2 = lines[1] if len(lines) > 1 else ''
                data_3_3 = lines[2] if len(lines) > 2 else ''
                # continues if any ...

                # Combine data into a dictionary
                scraped_data = {
                    'data_1': data_1,
                    'data_2': data_2,
                    'data_3_1': data_3_1,
                    'data_3_2': data_3_2,
                    'data_3_3': data_3_3
                    # continues if any ...
                }
                
                # Append the dictionary to the scraped_list
                scraped_list.append(scraped_data)
            
            # Find and click the "Next" button
            next_button_path = 'xpath'
            try:
                page.wait_for_selector(next_button_path, timeout=60000)  
                next_page = page.query_selector(next_button_path)

                if next_page and next_page.is_enabled():
                    next_page.click()
                else:
                    print('===[No "Next page" button found. Exiting scraping]===')
                    break
            except Exception as e:
                print(f"Error: {e}")
                print('===[Error while waiting for the "Next page" button. Exiting scraping]===')
                break

            # Wait for the page to load
            page.wait_for_load_state('networkidle', timeout=60000)
        
        print('===[Scraping Succesful]===')
        browser.close() 
                
        # Create a pandas DataFrame
        df = pd.DataFrame(scraped_list)

        # Save the DataFrame to a CSV file
        df.to_csv('your_csv_file_name.csv', index=False)

# Checks whether the current module is being executed as the main program
if __name__ == '__main__':
    main()


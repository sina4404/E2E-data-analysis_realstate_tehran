# Tehran Real Estate Analysis

This is an end-to-end project, covering data scraping, cleaning, modeling, and visualization.
- You can find visualizations in the `eda` folder.
- You can find modeling in the `modeling` folder.
- How is the data cleaned? `cleaning` folder.
- Data Collection, `scraping` folder.

This project involves scraping data from a real estate finding home website. The dataset contains over 3000 rows with various columns such as area, building year, floor number, parkings, storage, price, and location. The data was scraped on 05/11/1403 (Shamsi calendar).

## Data Description

The dataset includes the following columns:
- **Area**
- **Building Year**
- **Floor Number**
- **Parkings** 
- **Storage** 
- **Price**
- **Location**
  
## Cloning the Repository
  ```bash
  git clone https://github.com/sina4404/E2E-data-analysis_realstate_tehran.git
  ```
## Running the Scraped Data

To run the scraped data, follow these steps:

1. Navigate to the scraping directory:
    ```bash
    cd scraping
    ```

2. Create a virtual environment:
    ```bash
    python -m venv env
    ```

3. Activate the virtual environment:
    - On Windows:
        ```bash
        .\env\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source env/bin/activate
        ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the scraping script:
    ```bash
    python data_scraper.py
    ```

## Dependencies

This project uses SeleniumBase for web scraping. Ensure that you have the following installed:

```python
from seleniumbase import Driver

Note: This project requires additional machine learning libraries for analysis and visualization.

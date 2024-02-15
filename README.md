# TECHIN 510 Lab 5
A world clock app that displays time in different locations around the world

## How to run
**Method 1:**
Open [luoyi-techin510-lab5.azurewebsites.net](https://luoyi-techin510-lab5.azurewebsites.net) in brower

**Method 2:**
Open the terminal and run the following commands:
```
pip install -r requirements.txt
streamlit run app.py
```

### What's Included
- `scraper.py`: Scrap and handle information on https://visitseattle.org/events
- `requirements.txt`: Required packages to run the application
- `app.py`: The main Seattle Events app.
    - The first part of the app shows the upcoming 6 events based on applied filter. The events can be filtered by category, region and date range. It will display event information as well as their venue in map.
        - In order to get a more precised coordinate, I implemented GoogleMaps API to obtain the venue's coordinate for each event.
    - The second part of the app contains some general event statistic, including event category distribution and top 10 venues with the most events.
- `db.py`: The main Seattle Events app.
- `dataviz.ipynb`: Contains the code for the data visualization practices
- `eda.ipynb`: Contains the code for the data handleing practices

### Lessions Learned
- How to store and obtain SQL data from Azure database
- How to make use of "container" in Streamlit to create a card-like UI
- How to visualize data using altair and folium
- How to implement packages like altair, folium on streamlit


### Questions
- Is there any way to put percetage numbers and labels on the pie chart using altair?
- How to costomize the text style in the folium marker popup?
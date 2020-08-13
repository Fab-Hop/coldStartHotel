# coldStartHotel

This project 

## Structure

## Installation

### Data Download
The actual TripAdvisor dataset is not published as part of this project, because it is an external resource avalible at https://doi.org/10.13140/RG.2.2.10285.90083

The following commands will download, unzip and rename the dataset: 
```
wget -P data/. "https://www.researchgate.net/profile/Matthias_Braunhofer/publication/308968574_TripAdvisor_Dataset/data/57fb7b7008ae91deaa685237/TripAdvisor-Dataset.zip"
unzip data/TripAdvisor-Dataset.zip -d data/
mv data/ratingswithcontextandmetadata.csv data/tripadvisor.csv
```

### Python
The project uses Python 3. The required libaries are saved to the `requirements.txt` file and can be install with `pip install -r requirements.txt'  

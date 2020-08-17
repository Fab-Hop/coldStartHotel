# coldStartHotel

This project illustrates the usage of schema level expert knowledge represented in a knowledge graph to define user-specific item subclasses, which are used to generate suitable recommendations based on representative user restrictions on the example of hotel recommendations.

## Structure
* `data`
 * `combined.ttl`: Abox and Tbox of the recommender system.
 * `inferredInstances.ttl`: Result of DL reasoner.
 * `recommenderClasses.ttl`: Tbox of the recommender system.
 * `tripadvisor.csv`: instance dataset.
 * `tripadvisor.ttl`: converted TripAdvisor dataset by utilizing schema.org classes. 
 * `TripAdvisor-Dataset.zip`: zipped instance dataset. 
* `extractTripAdvisorData.py`: Reads TripAdvisor dataset and creates corresponding triples, which can be used 
* `requirements.txt`: Python requirements for `extractTripAdvisorData.py` script. 

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
The project uses Python 3. The required libaries are saved to the `requirements.txt` file and can be install with `pip install -r requirements.txt'. 

## Create Recommendations

### Extract data
Run the `extractTripAdvisorData.py` script. 
### Combine RecommenderClasses and instances
Merge the extracted triple with the defined hotel subclasses. 
### Run DL reasoner
Run a reasoner on the combined file. The results are obtained with FaCT 1.6.5. 


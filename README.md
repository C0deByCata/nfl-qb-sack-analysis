# NFL Sacks Analysis

Repository for analyzing NFL sacks data.

## Data Source
Download the data from [https://www.pro-football-reference.com/](https://www.pro-football-reference.com/). The games data is available in the `raw_data/nfl_games` directory and boxscore data in the `raw_data/boxscores_prr` directory.
The processed data for the analysis is in the file `processed_data.csv`.

## Visualization
Visualizations are created using Streamlit and Plotly. To run the Streamlit app, use the following command:

```bash
streamlit run __main__.py
```

## Requirements
Install the project using poetry:

```bash
poetry install
```

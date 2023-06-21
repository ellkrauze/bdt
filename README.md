# Mushrooms Family Classification
ITMO course project for Big Data Infrastructure subject

# Mushroom Family Classification

This repository contains the code and resources for a project on mushroom family classification. The goal of the project is to develop a model that can predict the family of a mushroom species based on its image and taxonomic features.

## Dataset

The project utilizes two main datasets:

1. **Image Dataset**: A collection of mushroom images labeled with their corresponding family. The images were gathered from various sources and preprocessed to ensure consistency and quality.

2. **Taxonomy Dataset**: A dataset containing taxonomic information about mushroom species, including family, order, class, phylum, and kingdom. This dataset also includes information on the edibility of each species.

Both datasets are combined to train and evaluate the classification model, leveraging both visual and taxonomic information for accurate predictions.

## Usage
Parser. Step 1

In the terminal write:
`celery -A app.celery worker --loglevel=info
flask run`

## Results

The project aims to achieve high accuracy in predicting the mushroom family based on the combined image and taxonomic features. The evaluation metrics and visualizations will help assess the model's performance and gain insights into the classification task.

## Acknowledgments

We would like to acknowledge the sources of the image and taxonomy datasets used in this project. Without their contributions, this project would not have been possible.

import requests
import pandas as pd
from flask import Flask
from celery import Celery, Task
from tqdm import tqdm
import time
import glob
import logging

app = Flask(__name__)

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.ERROR)


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


app.config.from_mapping(
    CELERY=dict(
        broker_url='redis://localhost:6379',
        # result_backend='redis://localhost:6379/0',
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)


class ImageDownloader:
    def __init__(self, csv_file, download_directory):
        self.csv_file = csv_file
        self.download_directory = download_directory
        self.df = pd.read_csv(csv_file)
        self.downloaded_images = set()  # Track downloaded image URLs

        # Load already downloaded images from the download directory
        self.load_downloaded_images()

    def load_downloaded_images(self):
        # Load already downloaded images from the download directory
        downloaded_files = glob.glob(f'{self.download_directory}/*.jpg')
        self.downloaded_images = set(downloaded_files)

    def download_images(self):
        new_images = 0
        for idx, row in tqdm(self.df.iterrows(), total=self.df.shape[0]):
            image_filename = f'{self.download_directory}/{idx}.jpg'
            if image_filename in self.downloaded_images:
                continue  # Skip if image already downloaded

            url = row.image
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            }
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to download image: {url}, due to: {str(e)}")
                continue

            if not response.ok:
                logging.error(f"Failed to download image: {url}, status code: {response.status_code}")
            else:
                new_images += 1
                try:
                    with open(image_filename, 'wb') as handle:
                        handle.write(response.content)
                    # Track newly downloaded image
                    self.downloaded_images.add(image_filename)
                except IOError as e:
                    logging.error(f"Failed to write file: {image_filename}, due to: {str(e)}")

        print(f"{new_images} images downloaded successfully!")


@celery_app.task
def run_image_downloader(csv_file, download_directory):
    downloader = ImageDownloader(csv_file, download_directory)
    downloader.download_images()


@app.route('/')
def start_image_downloader():
    csv_file = 'MO MI images - imagesAndNames.csv'
    download_directory = './data_test'
    run_image_downloader.delay(csv_file, download_directory)
    return "Image downloader has started!"


if __name__ == '__main__':
    app.run(debug=True)
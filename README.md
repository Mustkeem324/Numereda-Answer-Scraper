# Numereda Answer Scraper

![GitHub repo size](https://img.shields.io/github/repo-size/Mustkeem324/PHP-Chegg-Answer-Scraper)
![GitHub contributors](https://img.shields.io/github/contributors/Mustkeem324/PHP-Chegg-Answer-Scraper)
![GitHub stars](https://img.shields.io/github/stars/Mustkeem324/PHP-Chegg-Answer-Scraper?style=social)
![GitHub forks](https://img.shields.io/github/forks/Mustkeem324/PHP-Chegg-Answer-Scraper?style=social)
[![Twitter Follow](https://img.shields.io/twitter/follow/Mustkee54967794?style=social)](https://twitter.com/Mustkee54967794)

This Python Flask application serves as an API for scraping answers from the Numereda website. It takes a Numereda question URL as input and returns the question along with its answer and any associated video.

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the project directory:

    ```bash
    cd numereda-answer-scraper
    ```

3. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the Flask server by running:

    ```bash
    python app.py
    ```

2. Access the API by making a GET request to the following endpoint:

    ```
    http://localhost:5000/apii?url=(numereda_question_url)
    ```

    Replace `(numereda_question_url)` with the URL of the Numereda question you want to scrape.

3. The API will return HTML content containing the scraped question, answer, and associated video (if available).

## API Documentation

### Endpoint: `/apii`

#### Method: GET

#### Parameters:

- `url` (required): The URL of the Numereda question you want to scrape.

#### Response:

- If successful, returns HTML content with the scraped question, answer, and video.
- If the video is not found, returns a 400 error message.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add your feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Create a new Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

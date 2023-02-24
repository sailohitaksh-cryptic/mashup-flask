# Mashup WebApp

This is a Mashup WebApp that allows you to create a mashup of audio clips from YouTube videos of a particular singer. The application is built using Python and Flask and is deployed on Azure. 

## How to Use

To use the application, follow the steps below:

1. Enter the singer's name, number of videos, and duration to be clipped in the appropriate fields.
2. Enter your email address.
3. Click on the "Create Mashup" button.
4. Wait for the application to search for the YouTube videos of the singer, download them, convert them to audio, and create the mashup.
5. Download the final mashup audio file.

## Dependencies

The following packages are required to run the application:

- Flask
- Pytube
- Audiosegment
- Youtubesearch

All of these packages are included in the `requirements.txt` file.

## Installation

To install the application, follow the steps below:

1. Clone the repository.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Run the application using the command `python app.py`.
4. Access the application at `http://localhost:5000` in your web browser.

## Deployment

The application is deployed on Azure. To deploy the application, follow the steps below:

1. Create an Azure account and sign in.
2. Create a new web app and select Python as the runtime stack.
3. Configure the deployment source as the GitHub repository where the application is stored.
4. Click on the "Deploy" button to deploy the application.
5. Access the deployed application at the URL provided by Azure.

## Credits

This application was created by [Your Name] using Python, Flask, Pytube, Audiosegment, and Youtubesearch. 

## License

This application is licensed under the [MIT License](https://opensource.org/licenses/MIT).

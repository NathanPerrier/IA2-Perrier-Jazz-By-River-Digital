# ATC BOOKING SITE

Created by [Nathan Perrier](https://github.com/nathan-perrier23) of [Ambrose Treacy College](https://www.atc.qld.edu.au/)

IA2 - Digital Solutions - Year 12 - QCAA

## Description

This is an event booking and ticketing website for Ambrose Treacy College, a Brisbane Boys School. The website allows users to book tickets for various events organized by the school. It is built using Django framework and follows the MVC design pattern. The website also includes user authentication features to ensure secure access to the booking system.

The application uses various APIs and AI technologies to provide users with accurate and up-to-date data.

This website was built upon the previous repositories:

- [IA1-Weather-App-Django](https://github.com/nathan-perrier23/IA1-Weather-App-Django)
- [Y11-T4-ATC-Blogging-Website](https://github.com/nathan-perrier23/Y11-T4-ATC-Blogging-Website)

The application's design is user-friendly and intuitive, making it easy for users to navigate and find the information they're looking for. The design is also responsive, ensuring a seamless experience on desktop, tablets, and mobile devices.

## Features

- Book Jazz By the River event
- User authentication.
- Responsive design that works on desktop, tablets, and mobile.
- Integration with various AI's for a better user experience.
- User-friendly and intuitive design inspired by modern sites.
- Routes and directions based on local weather.

## How to Run

### Running the Django Application Locally

1. Ensure you have Python 3.8 or later installed on your machine. You can download it from [here](https://www.python.org/downloads/).

2. Clone the Github repository using:

    `git clone https://github.com/nathan-perrier23/IA2-Perrier-Jazz-By-River-Digital.git`

3. Set up environment variables for configuration. These are stored in a `.env` file at the root of the        
    project. You'll need to create this file and add the following parameters. REMEMBER to change the API values and to `create a Google project with VertexAI API enabled, also enable google places api`:

    ```properties
    CELERY_BROKER_URL = 'redis://:A45H2sg23hd2hdjhAG211hkyJKJ89@localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:A45H2sg23hd2hdjhAG211hkyJKJ89@localhost:6379/0'
    REDIS_HOST = 'redis'
    REDIS_BACKEND = 'redis://192.168.68.55:6379'

    SECRET_KEY = 'your-secret-key'

    OPENAI_API_KEY = 'your-openai-api-key'

    MAPBOX_ACCESS_TOKEN = 'your-mapbox-access-token'

    EMAIL_HOST_USER = 'your-gmail-email'
    EMAIL_HOST_PASSWORD = 'your-gmail-app-password'
   
    GOOGLE_PROJECT_ID = 'your-google-project-id'

    GOOGLE_PLACES_API_KEY = 'your-google-places-api-key'

    DJANGO_SETTINGS_MODULE= atc_site.settings
    ```

    NOTE: To use a Gmail account to send emails, you must set up an app password - but to do this you first need to enable 2-Step Verification, then select ‘App passwords’ under ‘2-Step Verification’. You must also turn on the ‘Less Secure App Access’ option in your google account.

4.  create a virtual environment using `control + shift + p` then search create environment. After you have created the venv then restart vs code. Might need:

    ```sh
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force;
    ```
    
    and

    ```sh
    ./.venv/scripts/activate
    ```

5. Install the required Python packages using pip:

    ```sh
    pip install -r requirements.txt
    ```

6. You will need to mirgrate the app using:

    ```sh
    python manage.py makemigrations
    ```
    then after that use:
    ```sh
    python manage.py migrate
    ```

    or if that did not work try use:

    ```sh
    docker-compose run app python manage.py makemigrations
    ``` 

    then after that use: 

    ```sh
    docker-compose run app python manage.py migrate
    ```

7. Navigate to the project directory and run the Django server:

    ```sh
    python manage.py runserver
    ```

8. Open your web browser and visit `http://127.0.0.1:8000/`.

### Running the Application Using Docker

1. Ensure you have Docker (and optionally Docker Desktop) installed on your machine. You can download it from [here](https://www.docker.com/products/docker-desktop). Make sure you start docker using `sudo service docker start`

2. Clone the Github repository using:

    `git clone https://github.com/nathan-perrier23/IA2-Perrier-Jazz-By-River-Digital.git`

3. create a virtual environment using `control + shift + p` then search "create environment". After you have created the venv then restart vs code. Make sure you pip install libraries to the environment using `pip install -r requirements.txt`. Might need:

    ```sh
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force;
    ```

    and

    ```sh
    ./.venv/scripts/activate
    ```

4. Set up environment variables for configuration. These are stored in a `.env` file at the root of the        
    project. You'll need to create this file and add the following parameters. REMEMBER to change the API values and to `create a Google project with VertexAI API enabled and to also enable google places api`:

    ```properties
    CELERY_BROKER_URL = 'redis://:A45H2sg23hd2hdjhAG211hkyJKJ89@localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:A45H2sg23hd2hdjhAG211hkyJKJ89@localhost:6379/0'
    REDIS_HOST = 'redis'
    REDIS_BACKEND = 'redis://192.168.68.55:6379'

    SECRET_KEY = 'your-secret-key'

    OPENAI_API_KEY = 'your-openai-api-key'
    MAPBOX_ACCESS_TOKEN = 'your-mapbox-access-token'

    EMAIL_HOST_USER = 'your-gmail-email'
    EMAIL_HOST_PASSWORD = 'your-gmail-app-password'
    
    GOOGLE_PROJECT_ID = 'your-google-project-id'

    GOOGLE_PLACES_API_KEY = 'your-google-places-api-key'

    DJANGO_SETTINGS_MODULE= atc_site.settings
    ```

    NOTE: To use a Gmail account to send emails, you must set up an app password - but to do this you first need to enable 2-Step Verification, then select ‘App passwords’ under ‘2-Step Verification’. You must also turn on the ‘Less Secure App Access’ option in your google account.

5. You will need to mirgrate the app using:

    ```sh
    python manage.py makemigrations
    ```
    then after that use:
    ```sh
    python manage.py migrate
    ```

    or if that did not work try use:

    ```sh
    docker-compose run app python manage.py makemigrations
    ``` 

    then after that use: 

    ```sh
    docker-compose run app python manage.py migrate
    ```

6. Build the Docker image (ensure docker is running):

    ```sh
    docker build -t atc_site -f DockerFile .
    ```

7. Run the Docker container:

    For Deployment, use:

    ```sh
    docker run -p 8000:8000 atc_site
    ```

    or 

    ```sh
    docker compose watch
    ```

    For Development:

    ```sh 
    docker run -p 8000:8000 -v "$(pwd):/app" atc_site
    ```

8. Open your web browser and visit `http://localhost:8000/`.

9. When you make changes, you will need to rebuild the Docker images and restart the Docker containers. You can do this with `docker-compose down` and then `docker-compose up --build`.

### NOTE

If you are using the Docker Toolbox, you will need to visit the IP address of the Docker Machine instead of `localhost`. You can find the IP address by running `docker-machine ip` in the terminal.

 Use `docker system prune -a` to remove all unused containers, networks, images (both dangling and unreferenced), and optionally, volumes.

## Resources and References

This Project utilised various projects and resources, that can be seen in the [REFERENCES](REFERENCES.md) file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
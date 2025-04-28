# Flask Campaign App

## Overview
The Flask Campaign App is a web application that allows users to manage campaigns, upload media files, and configure advertisements. The application features a simple login screen, a gallery for uploading images, GIFs, and videos, and a campaign configuration interface that supports the creation of multiple campaigns and ads.

## Features
- User authentication with a login screen.
- Media gallery for uploading and managing images, GIFs, and videos.
- Campaign configuration screen to create and manage up to 100 campaigns, each containing 6 ads with the ability to hold 6 media files each.

## Project Structure
```
flask-campaign-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── js
│   │   │   └── scripts.js
│   └── templates
│       ├── base.html
│       ├── login.html
│       ├── gallery.html
│       └── campaign_config.html
├── instance
│   └── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-campaign-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration
- Update the `instance/config.py` file with your database connection details and secret keys.

## Running the Application
To run the application, execute the following command:
```
python run.py
```
The application will be accessible at `http://127.0.0.1:5000`.

## Usage
- Navigate to the login page to authenticate.
- After logging in, you can access the media gallery to upload files.
- Use the campaign configuration screen to create and manage your campaigns and ads.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.
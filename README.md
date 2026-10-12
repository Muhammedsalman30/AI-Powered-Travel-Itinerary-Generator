# AI-Powered Travel Itinerary Generator ✈️

## Project Overview

An AI-powered travel itinerary generator developed
using Python and Streamlit.

The application generates personalized travel
itineraries based on customer requirements such
as destination, budget, travel duration and interests.

## Features

- Customer information collection
- AI-powered itinerary generation using Gemini API
- Personalized travel recommendations
- PDF itinerary generation
- SQLite customer database
- Customer CRUD operations
- Search and manage customer records

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- SQLite
- ReportLab
- Pandas

## Project Workflow

1. Customer enters travel requirements.
2. Gemini AI generates a travel itinerary.
3. The itinerary is displayed in Streamlit.
4. Customer information is stored in SQLite.
5. ReportLab generates a downloadable PDF.
6. Operations team verifies the itinerary.

## Installation

Clone the repository:

git clone YOUR_GITHUB_REPOSITORY_URL

Install dependencies:

pip install -r requirements.txt

Create a .env file and add:

GEMINI_API_KEY=your_api_key

Run the application:

streamlit run app.py

## Important Note

The generated itineraries are drafts.
All travel information, prices and availability
must be verified by the operations team.

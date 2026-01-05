# NutriCoach

A Desktop Co-Pilot application which focuses on providing and explaining ingredient information of any food, prioritizing user experience and quality reasoning. It analyzes ingredient text or labels and explains health impact, trade-offs, and uncertainties using evidence-based retrieval and Gemini AI.

## Description

-   NutriCoach can give consumers insights about ingredients found in labels of products they buy.

-   People usually have problems reading labels when they are deciding whether to buy a product or not.

-   Most of them have chemical labels which doesn't specify why an ingredient is added.

-   Here comes NutriCoach in action, it takes the ingredient lists as input, and explains what the ingredients mean and why they are added.

-   It explains the tradeoffs, and mentions if any healh issues are caused by the ingredients without making an absolute claims.

-   The model answers to the consumer with minimal input from the consumer.

-   This is what makes NutriCoach different from other AI-powered applications already available.

## Features
- AI Ingredient Analysis (powered by Gemini)
- Evidence-based explanations (RAG: Retrieval Augmented Generation)
- Paste ingredients or upload label images
- Smart follow-up questions (kids safety, cautions, alternatives)
- Clean PyQt5 desktop UI
- Light / Dark mode support for chat
  
## Technologies Used

-   Frontend - **PyQt, Python**, 

-   Backend - **Django, Django Rest Framework**

-   AI - **Google Gemini API, RAG**

-   OCR - **Tesseract+ pytesseract**

## Architecture Overview
- Frontend: PyQt5 desktop application, handling user input, file uploads, and UI rendering
- Backend: Django REST API, Ingredient retrieval using embeddings, Gemini model for natural language explanation
- 
  Frontend (PyQt5)
   ↓ HTTP
  Backend (Django API)
   ↓
  Embedding Retrieval + Gemini AI


## Product Workflow
- User enters ingredient text or uploads a label image

- Backend retrieves relevant ingredient knowledge using embeddings

- Gemini AI generates: Summary, Details, Uncertainty

- Follow-up questions refine the same ingredient context or new conversation by text or image upload of another ingredient

## 🛠️ Installation & Setup (WINDOWS)
1️ Clone the repository:
- git clone https://github.com/Anwesha-TU/NutriCoach.git
- cd NutriCoach

2️ Create virtual environment:
- python -m venv venv
- venv\Scripts\activate

3️ Install dependencies:
- pip install -r requirements.txt

4 OCR Support: 
- Install Tesseract OCR (Windows)
- Add path in code:
- pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

5 Set environment variable:
- Create a .env file in the backend folder:
GEMINI_API_KEY=your_api_key_here

6 Run Backend Server:
- cd backend
- python manage.py runserver

7 Run Frontend: 
- python frontend.py
### OR
- Run the application from dist/frontend.exe

## Model Building and Workflow

-   `Data Collection`: We collected about 20-30 ingredients details and saved them in **JSON** format.
-   `Data Preprocessing`: From the JSON data, the data was converted into numerical format with the help of an embedding model. These are called _Vecor Embeddings_.
-   `User Query`: Consumers paste their ingredients list and that becomes our user query. It is converted to numerical format with the same embedding model used to create vector embeddings.
-   `Retrieval`: **Cosine Similarity** is used to match the user query vector to all the embeddings and select the `k` closest matches. These k matches are our context.
-   `Generation`: Then, the generative model replies using the context, and if there is no context, then the model will say so without hallucinating.

## Limitations
- Gemini Free-Tier has daily- request limits
- Image OCR quality depends on label clarity

## Warnings
Our tool is not a medical diagnostic tool, and the application provides educational insights only and does not replace professional medical or dietary advice.

## Contributors:
- Anwesha Chakraborty
- Koustav Chatterjee

# AI Expense Tracker

This is a simple and user-friendly expense tracker built using Python and Streamlit. It helps users manage their daily expenses by allowing them to enter data manually or by uploading receipts. The project also shows visual charts and gives budget suggestions based on the user's spending.

---

## Features

- Add your expenses with description, amount, date, and category.
- Upload receipt images and extract text using OCR (EasyOCR).
- See where your money is going through pie charts and bar graphs.
- Track your monthly and yearly expenses.
- Get basic suggestions based on your monthly budget.

---

## Tools & Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib
- NumPy
- EasyOCR
- Pillow (for image processing)

---

## AI/ML Integration (Internship Requirement Justification)
In this project, I used EasyOCR, which is a deep learning-based tool, to read and extract text from receipt images.
This is an example of how AI is used in real life, especially in the area of computer vision.
The app takes an image, finds the text using AI, and turns it into useful data for tracking expenses.

This clearly shows the use of Artificial Intelligence, which is one of the main requirements of the internship.

Even though the app runs locally now, it is designed in a way that it can be deployed on Microsoft Azure in the future, using services like:

🔹Azure Cognitive Services (for OCR)

🔹Azure Blob Storage (to store receipt images)

🔹Azure App Services (to make the app live)

## How to Run the Project

1. Clone the repository: git clone https://github.com/chilukadivya/AI-Expense-Tracker.git cd AI-Expense-Tracker
2. Install the required libraries: pip install -r requirements.txt
3. Run the app: streamlit run ai_expense_tracker.py


---

## Screenshots

Here are a few screenshots from the app:

- Expense Entry Form  
- Receipt Upload and OCR  
- Category-wise and Monthly Charts  
- Budget Suggestions

(You can find them in the "screenshots" folder.)

---

## Notes

- This project is developed as part of the Edunet Foundation Internship under Microsoft AI-Azure.
- As mentioned in the internship video, **deployment is optional**. This app works perfectly on local machines.
- All features were tested using sample data and receipt images.

---

## Submitted by

**Name:** Chiluka Divya  
**College:** Kasturba Gandhi Degree & PG College for Women  
**Internship:** Edunet Foundation - Microsoft AI & Azure  
**Project Title:** AI Expense Tracker




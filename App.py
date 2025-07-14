import streamlit as st
import pandas as pd
import os
from datetime import date 
import re
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image



# Title and page config
st.set_page_config(page_title="AI Expense Tracker", layout="centered")
st.title(" AI Expense Tracker")
st.write("Track your expenses with ease!")

# CSV path
file_path = "expenses.csv"

# If file doesn't exist, create it
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=["Date", "Amount", "Description","Category"])
    df.to_csv(file_path, index=False)


# Load existing expense data
data = pd.read_csv(file_path) if os.path.exists(file_path) else pd.DataFrame(columns=["Date", "Amount", "Description", "Category"])


# Convert and enrich date columns
#data = pd.read_csv(file_path) if os.path.exists(file_path) else pd.DataFrame(columns=["Date", "Amount", "Description", "Category"])
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data['Month'] = data['Date'].dt.to_period('M').astype(str)
data['Year'] = data['Date'].dt.year.astype(str)
data['Category'] = data['Category'].str.strip()  # 👈 This fixes label formatting



# Expense entry form
with st.form("entry_form", clear_on_submit=True):
    st.subheader(" Add New Expense")
    description = st.text_input("Description (e.g., Paid ₹500 for groceries)")
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    expense_date = st.date_input("Date", value=date.today())
    category = st.selectbox("Category", ["groceries", "food", "travel", "bill", "rent", "other"]) 
    submitted = st.form_submit_button("Save Expense")

if submitted:
    new_data = pd.DataFrame([[expense_date, amount, description, category]],
    columns=["Date", "Amount", "Description", "Category"])
    new_data.to_csv(file_path, mode='a', header=False, index=False)
    st.success(" Expense saved successfully!")


    



# Upload and extract receipt using EasyOCR

st.subheader("Upload and Extract Text from Receipt")

uploaded_file = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)

    # Convert to numpy array
    image_np = np.array(image)

    # OCR with EasyOCR
    with st.spinner("Extracting text from image..."):
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(image_np)

    # Combine extracted text
    extracted_text = "\n".join([text for _, text, _ in results])
    
    st.subheader(" Extracted Text")
    st.text_area("Text from Receipt", extracted_text, height=200)

#  Upload and extract receipt using EasyOCR

if st.button(" Save Extracted as Expense"):
    if extracted_text.strip():
        amounts = re.findall(r'₹?\s?[\d,]+\.\d{2}', extracted_text)
        clean_amounts = [float(amt.replace("₹", "").replace(",", "").strip()) for amt in amounts if amt.replace("₹", "").replace(",", "").strip().replace(".", "").isdigit()]

        final_amount = max(clean_amounts) if clean_amounts else 0.0

        new_data = pd.DataFrame([[date.today(), final_amount, extracted_text.strip(), "other"]],
                                columns=["Date", "Amount", "Description", "Category"])
        new_data.to_csv(file_path, mode='a', header=False, index=False)

        st.success(f" Extracted text saved with amount ₹{final_amount:.2f}")
    else:
        st.warning(" No text detected in the receipt.")


st.subheader(" Spending Overview")

# Side-by-side charts
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("####  Category-wise Spending")
    category_totals = data.groupby("Category")["Amount"].sum()
    if not category_totals.empty:
        fig1, ax1 = plt.subplots()
        ax1.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)
    else:
        st.info("Add some expenses to visualize category distribution.")

with col2:
    st.markdown("####  Monthly Totals")
    monthly_totals = data.groupby("Month")["Amount"].sum().reset_index()
    if not monthly_totals.empty:
        st.bar_chart(monthly_totals.set_index("Month"))
    else:
        st.info("Monthly data will appear once expenses span more than one month.")

# ────────────── Expandable insights ──────────────
with st.expander(" Yearly Expense Trend"):
    yearly_totals = data.groupby("Year")["Amount"].sum().reset_index()
    if not yearly_totals.empty:
        st.line_chart(yearly_totals.set_index("Year"))
    else:
        st.info("Yearly trend will activate once your data spans multiple years.")

with st.expander(" Smart Suggestions"):
    st.markdown("###  Enter Your Monthly Budget")
    monthly_budget = st.number_input(
        "Monthly Budget (₹)", 
        min_value=0.0, 
        format="%.2f", 
        value=20000.0,  
        key="budget_input"
    )

    current_month = data['Month'].iloc[-1] if not data.empty else None
    if current_month:
        this_month_expenses = data[data['Month'] == current_month]
        spent_this_month = this_month_expenses['Amount'].sum()
        leftover = monthly_budget - spent_this_month
        top_cats = this_month_expenses.groupby("Category")["Amount"].sum().nlargest(3)

        st.markdown(f"**Budget:** ₹{monthly_budget:,.2f}")
        st.markdown(f"**Spent:** ₹{spent_this_month:,.2f}")
        st.markdown(f"**Leftover:** ₹{leftover:,.2f}")

        if not top_cats.empty:
            st.markdown("**Top Spending Areas:**")
            for cat, amt in top_cats.items():
                st.markdown(f"- `{cat}`: ₹{amt:,.2f}")

        if leftover > 0:
            st.success("You're within budget — great time to save or invest!")
        elif leftover < 0:
            st.warning("Overspent this month — consider adjusting next month’s budget.")
        else:
            st.info("Perfect balance.")
    else:
        st.warning("No expense data available to generate suggestions.")
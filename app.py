import streamlit as st
import pandas as pd

from travel_ai import generate_itinerary

from database import (
    create_table,
    add_customer,
    get_customers,
    search_customer,
    update_customer,
    delete_customer
)

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from xml.sax.saxutils import escape

from io import BytesIO


# ==================================
# 1. PAGE CONFIGURATION
# ==================================

st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="✈️",
    layout="centered"
)

# Initialize database
create_table()

st.title("✈️ AI Travel Itinerary Generator")

st.write(
    "Generate personalized travel itineraries "
    "using Artificial Intelligence."
)


# ==================================
# 2. CUSTOMER INFORMATION
# ==================================

st.subheader("Customer Information")

name = st.text_input("Customer Name")

email = st.text_input("Email Address")


# ==================================
# 3. TRAVEL REQUIREMENTS
# ==================================

st.subheader("Travel Requirements")

destination = st.text_input(
    "Travel Destination",
    placeholder="Example: Paris, France"
)

days = st.number_input(
    "Number of Travel Days",
    min_value=1,
    max_value=30,
    value=3
)

budget = st.selectbox(
    "Budget",
    [
        "Budget Friendly",
        "Standard",
        "Premium"
    ]
)

interests = st.multiselect(
    "Travel Interests",
    [
        "Sightseeing",
        "Museums",
        "Shopping",
        "Adventure",
        "Food",
        "Nature"
    ]
)


# ==================================
# 4. GENERATE AI ITINERARY
# ==================================

if st.button("Generate Travel Itinerary"):

    if not name.strip() or not destination.strip():

        st.error(
            "Please enter customer name and destination."
        )

    else:

        try:

            # Generate itinerary using Gemini

            with st.spinner(
                "Gemini AI is generating your itinerary..."
            ):

                ai_result = generate_itinerary(
                    destination,
                    int(days),
                    budget,
                    interests
                )

            if not ai_result:

                st.error("AI returned an empty response.")

            else:

                # ----------------------------
                # SAVE CUSTOMER TO SQLITE
                # ----------------------------

                customer_id = add_customer(
                    name,
                    email,
                    destination,
                    int(days),
                    budget,
                    interests,
                    ai_result
                )

                st.success(
                    f"Customer saved successfully! ID: {customer_id}"
                )

                # ----------------------------
                # CUSTOMER DETAILS
                # ----------------------------

                st.subheader("Customer Details")

                st.write("Customer:", name)

                st.write("Email:", email)

                st.write("Destination:", destination)

                st.write("Duration:", days, "days")

                st.write("Budget:", budget)

                st.write(
                    "Interests:",
                    ", ".join(interests)
                )

                # ----------------------------
                # DISPLAY AI RESULT
                # ----------------------------

                st.subheader(
                    "AI Generated Travel Itinerary"
                )

                st.markdown(ai_result)

                # ----------------------------
                # CREATE PDF
                # ----------------------------

                buffer = BytesIO()

                pdf = SimpleDocTemplate(
                    buffer,
                    pagesize=A4,
                    rightMargin=45,
                    leftMargin=45,
                    topMargin=45,
                    bottomMargin=45
                )

                styles = getSampleStyleSheet()

                content = []

                content.append(
                    Paragraph(
                        "TRAVEL ITINERARY",
                        styles["Title"]
                    )
                )

                content.append(Spacer(1, 20))

                content.append(
                    Paragraph(
                        f"<b>Customer:</b> {escape(name)}",
                        styles["Normal"]
                    )
                )

                content.append(
                    Paragraph(
                        f"<b>Email:</b> {escape(email)}",
                        styles["Normal"]
                    )
                )

                content.append(
                    Paragraph(
                        f"<b>Destination:</b> {escape(destination)}",
                        styles["Normal"]
                    )
                )

                content.append(
                    Paragraph(
                        f"<b>Duration:</b> {days} days",
                        styles["Normal"]
                    )
                )

                content.append(
                    Paragraph(
                        f"<b>Budget:</b> {escape(budget)}",
                        styles["Normal"]
                    )
                )

                content.append(Spacer(1, 25))

                content.append(
                    Paragraph(
                        "AI GENERATED ITINERARY",
                        styles["Heading2"]
                    )
                )

                content.append(Spacer(1, 15))

                for line in ai_result.splitlines():

                    line = line.strip()

                    if line:

                        content.append(
                            Paragraph(
                                escape(line),
                                styles["BodyText"]
                            )
                        )

                        content.append(Spacer(1, 8))

                content.append(Spacer(1, 25))

                content.append(
                    Paragraph(
                        "Operations Team Verification",
                        styles["Heading2"]
                    )
                )

                content.append(
                    Paragraph(
                        "This is a draft itinerary. "
                        "All travel information, prices, "
                        "availability and booking details "
                        "must be verified by the operations team.",
                        styles["Italic"]
                    )
                )

                # Generate PDF

                pdf.build(content)

                buffer.seek(0)

                st.download_button(
                    label="📄 Download Travel Itinerary PDF",
                    data=buffer,
                    file_name="travel_itinerary.pdf",
                    mime="application/pdf"
                )

                st.success(
                    "Your travel itinerary PDF is ready!"
                )

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )

            st.info(
                "Check your Gemini API connection and application settings."
            )


# ==================================
# 5. CUSTOMER MANAGEMENT DASHBOARD
# ==================================

st.divider()

st.title("📊 Customer Management")

menu = st.selectbox(
    "Select Operation",
    [
        "View Customers",
        "Search Customers",
        "Update Customer",
        "Delete Customer"
    ]
)


# ==================================
# 6. VIEW CUSTOMERS
# ==================================

if menu == "View Customers":

    customers = get_customers()

    if customers:

        df = pd.DataFrame(
            [dict(customer) for customer in customers]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.metric(
            "Total Customers",
            len(customers)
        )

    else:

        st.info("No customer records found.")


# ==================================
# 7. SEARCH CUSTOMERS
# ==================================

elif menu == "Search Customers":

    keyword = st.text_input(
        "Enter customer name, email or destination"
    )

    if keyword:

        results = search_customer(keyword)

        if results:

            df = pd.DataFrame(
                [dict(customer) for customer in results]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.warning(
                "No matching customers found."
            )


# ==================================
# 8. UPDATE CUSTOMERS
# ==================================

elif menu == "Update Customer":

    customers = get_customers()

    if customers:

        customer_options = {
            f"{c['id']} - {c['name']} ({c['destination']})": c
            for c in customers
        }

        selected = st.selectbox(
            "Select Customer",
            list(customer_options.keys())
        )

        customer = customer_options[selected]

        with st.form("update_customer_form"):

            new_name = st.text_input(
                "Customer Name",
                value=customer["name"]
            )

            new_email = st.text_input(
                "Email",
                value=customer["email"] or ""
            )

            new_destination = st.text_input(
                "Destination",
                value=customer["destination"]
            )

            new_days = st.number_input(
                "Travel Days",
                min_value=1,
                max_value=30,
                value=customer["days"] or 1
            )

            budgets = [
                "Budget Friendly",
                "Standard",
                "Premium"
            ]

            current_budget = customer["budget"]

            budget_index = (
                budgets.index(current_budget)
                if current_budget in budgets else 0
            )

            new_budget = st.selectbox(
                "Budget",
                budgets,
                index=budget_index
            )

            submitted = st.form_submit_button(
                "Update Customer"
            )

            if submitted:

                if not new_name.strip() or not new_destination.strip():

                    st.error(
                        "Name and destination are required."
                    )

                else:

                    update_customer(
                        customer["id"],
                        new_name,
                        new_email,
                        new_destination,
                        int(new_days),
                        new_budget
                    )

                    st.success(
                        "Customer updated successfully!"
                    )

                    st.rerun()

    else:

        st.info(
            "No customers available to update."
        )


# ==================================
# 9. DELETE CUSTOMERS
# ==================================

elif menu == "Delete Customer":

    customers = get_customers()

    if customers:

        customer_options = {
            f"{c['id']} - {c['name']} ({c['destination']})": c
            for c in customers
        }

        selected = st.selectbox(
            "Select Customer to Delete",
            list(customer_options.keys())
        )

        customer = customer_options[selected]

        st.warning(
            f"You are about to delete customer: {customer['name']}"
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this customer."
        )

        if st.button("Delete Customer"):

            if confirm:

                delete_customer(customer["id"])

                st.success(
                    "Customer deleted successfully!"
                )

                st.rerun()

            else:

                st.warning(
                    "Please confirm before deleting."
                )

    else:

        st.info(
            "No customer records available."
        )
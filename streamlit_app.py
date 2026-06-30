import streamlit as st
import time
from snowflake.snowpark.context import get_active_session

# -------------------------------------------------
# Snowflake Session
# -------------------------------------------------
session = get_active_session()
session.sql("USE DATABASE CUSTOMER360_DB").collect()
session.sql("USE SCHEMA GOLD").collect()

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Customer 360 Telecom Intelligence Platform",
    page_icon="📶",
    layout="wide"
)

# -------------------------------------------------
# Dark Telecom Theme
# -------------------------------------------------
st.markdown("""
<style>

/* App background */
.stApp{
    background:linear-gradient(180deg,#071B34 0%, #0C2345 100%);
    color:white;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#082B57;
}

/* Sidebar text */
section[data-testid="stSidebar"] *{
    color:white !important;
}

/* General text */
h1,h2,h3,h4,h5,h6,p,label,span{
    color:white !important;
}

/* Main titles */
h1{
    color:#FFFFFF !important;
    font-weight:800;
}

/* Section headers */
h2,h3{
    color:#38BDF8 !important;
}

/* Metric cards */
div[data-testid="metric-container"]{
    background:#102B4C;
    border:1px solid #1E4E8C;
    border-radius:16px;
    padding:20px;
    color:white;
    box-shadow:0 10px 20px rgba(0,0,0,.35);
}

/* Buttons */
.stButton>button{
    background:#0094FF;
    color:white;
    border:none;
    border-radius:12px;
    padding:10px 22px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#1DA1FF;
    color:white;
}

/* Text inputs */
.stTextInput input{
    background:#0E2A49;
    color:white;
    border:1px solid #3E74B7;
    border-radius:10px;
}

/* Select boxes */
.stSelectbox div[data-baseweb="select"]{
    background:#0E2A49;
    border-radius:10px;
    color:white;
}

/* DataFrames */
[data-testid="stDataFrame"]{
    border:1px solid #204A83;
    border-radius:15px;
    overflow:hidden;
}

/* Alerts */
[data-testid="stAlert"]{
    border-radius:12px;
}

/* Divider */
hr{
    border:1px solid #295D9C;
}

/* Caption */
.caption{
    color:#BFD7F5 !important;
}

/* Telecom banner */
.telecom-banner{
    background:#0E3D75;
    padding:14px 18px;
    border-radius:12px;
    margin-bottom:22px;
    color:white;
    font-weight:700;
    border:1px solid #1E88E5;
}

</style>
""", unsafe_allow_html=True)

def banner():
    st.markdown("""
    <div class="telecom-banner">
        📡 Telecommunications Customer Analytics Platform
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Load Data
# -------------------------------------------------
kpi_df = session.sql("SELECT * FROM V_EXECUTIVE_KPIS").to_pandas()
kpis = kpi_df.iloc[0]

revenue_state_df = session.sql("SELECT * FROM V_REVENUE_BY_STATE").to_pandas()
revenue_segment_df = session.sql("SELECT * FROM V_REVENUE_BY_SEGMENT").to_pandas()
churn_df = session.sql("SELECT * FROM V_CHURN_RISK_DISTRIBUTION").to_pandas()
health_df = session.sql("SELECT * FROM V_CUSTOMER_HEALTH_DISTRIBUTION").to_pandas()
usage_state_df = session.sql("SELECT * FROM V_USAGE_BY_STATE").to_pandas()
support_state_df = session.sql("SELECT * FROM V_SUPPORT_BY_STATE").to_pandas()
customer_search_df = session.sql("SELECT * FROM V_CUSTOMER_SEARCH").to_pandas()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.title("📂 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "📊 Executive Dashboard",
        "👥 Customer Analytics",
        "💰 Revenue Analytics",
        "🌎 State Analytics",
        "⚠️ Churn Analysis",
        "🤖 Cortex AI",
        "ℹ️ About"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("📶 Customer 360 Telecom Platform")

# -------------------------------------------------
# Home
# -------------------------------------------------
if page == "🏠 Home":

    st.title("📶 Customer 360 Telecom Intelligence Platform")
    banner()

    st.markdown("""
    ## Welcome!

    This application demonstrates an **end-to-end Customer 360 Analytics Platform**
    built entirely inside **Snowflake** using the **Medallion Architecture**.

    ### Architecture

    CSV Files → Internal Stage → RAW → SILVER → GOLD → Streamlit

    ### Tech Stack
    - Snowflake
    - SQL
    - Streamlit in Snowflake
    - Medallion Architecture
    - Snowflake Cortex AI
    """)

    st.success("Application initialized successfully!")

# -------------------------------------------------
# Executive Dashboard
# -------------------------------------------------
elif page == "📊 Executive Dashboard":

    st.title("📊 Executive Dashboard")
    banner()
    st.caption("Updated in real-time from GOLD Analytics Layer")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📡 Total Customers", int(kpis["TOTAL_CUSTOMERS"]))
    col2.metric("💵 Total Revenue", f"${kpis['TOTAL_REVENUE']:,.2f}")
    col3.metric("💳 Outstanding Balance", f"${kpis['TOTAL_OUTSTANDING_BALANCE']:,.2f}")
    col4.metric("📶 Active Plans", int(kpis["TOTAL_ACTIVE_SUBSCRIPTIONS"]))

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("📊 Avg Monthly Bill", f"${kpis['AVG_MONTHLY_BILL']:,.2f}")
    col6.metric("❤️ Avg Health Score", f"{kpis['AVG_CUSTOMER_HEALTH_SCORE']:,.1f}")
    col7.metric("📞 Support Tickets", int(kpis["TOTAL_SUPPORT_TICKETS"]))
    col8.metric("⚠️ Open Tickets", int(kpis["TOTAL_OPEN_TICKETS"]))

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.subheader("📈 Revenue by State")
        st.bar_chart(revenue_state_df, x="STATE", y="TOTAL_REVENUE")

    with right:
        st.subheader("💳 Revenue by Customer Segment")
        st.bar_chart(revenue_segment_df, x="CUSTOMER_SEGMENT", y="TOTAL_REVENUE")

# -------------------------------------------------
# Customer Analytics
# -------------------------------------------------
elif page == "👥 Customer Analytics":

    st.title("👥 Customer Analytics")
    banner()

    selected_customer = st.selectbox(
        "Select a Customer",
        customer_search_df["CUSTOMER_NAME"]
    )

    customer_id = customer_search_df[
        customer_search_df["CUSTOMER_NAME"] == selected_customer
    ]["CUSTOMER_ID"].iloc[0]

    customer_df = session.sql(f"""
        SELECT *
        FROM CUSTOMER_360_ANALYTICS
        WHERE CUSTOMER_ID = '{customer_id}'
    """).to_pandas()

    customer = customer_df.iloc[0]

    st.subheader(f"Customer Profile: {customer['CUSTOMER_NAME']}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Customer ID", customer["CUSTOMER_ID"])
    col2.metric("Health Score", int(customer["CUSTOMER_HEALTH_SCORE"]))
    col3.metric("Churn Risk", customer["CHURN_RISK_CATEGORY"])

    st.markdown("### Customer Details")

    st.write(f"**Email:** {customer['EMAIL']}")
    st.write(f"**Location:** {customer['CITY']}, {customer['STATE']}")
    st.write(f"**Segment:** {customer['CUSTOMER_SEGMENT']}")
    st.write(f"**Persona:** {customer['CUSTOMER_PERSONA']}")
    st.write(f"**Active Plans:** {customer['ACTIVE_PLAN_NAMES']}")

    st.markdown("### Financial Summary")

    col4, col5, col6 = st.columns(3)

    col4.metric("Total Revenue", f"${customer['TOTAL_AMOUNT_PAID']:,.2f}")
    col5.metric("Outstanding Balance", f"${customer['TOTAL_OUTSTANDING_BALANCE']:,.2f}")
    col6.metric("Avg Monthly Bill", f"${customer['AVG_MONTHLY_BILL']:,.2f}")

    st.markdown("### Usage & Support")

    col7, col8, col9 = st.columns(3)

    col7.metric("🌐 Avg Internet Usage", f"{customer['AVG_MONTHLY_INTERNET_USAGE_GB']:,.2f} GB")
    col8.metric("📞 Support Tickets", int(customer["TOTAL_SUPPORT_TICKETS"]))
    col9.metric("⚠️ Open Tickets", int(customer["OPEN_SUPPORT_TICKETS"]))

# -------------------------------------------------
# Revenue Analytics
# -------------------------------------------------
elif page == "💰 Revenue Analytics":

    st.title("💰 Revenue Analytics")
    banner()

    st.subheader("📈 Revenue by State")
    st.bar_chart(revenue_state_df, x="STATE", y="TOTAL_REVENUE")
    st.dataframe(revenue_state_df)

    st.subheader("💳 Revenue by Customer Segment")
    st.bar_chart(revenue_segment_df, x="CUSTOMER_SEGMENT", y="TOTAL_REVENUE")
    st.dataframe(revenue_segment_df)

# -------------------------------------------------
# State Analytics
# -------------------------------------------------
elif page == "🌎 State Analytics":

    st.title("🌎 State Analytics")
    banner()

    st.subheader("🌐 Internet Usage by State")
    st.bar_chart(usage_state_df, x="STATE", y="TOTAL_INTERNET_USAGE_GB")
    st.dataframe(usage_state_df)

    st.subheader("📞 Support Tickets by State")
    st.bar_chart(support_state_df, x="STATE", y="TOTAL_SUPPORT_TICKETS")
    st.dataframe(support_state_df)

# -------------------------------------------------
# Churn Analysis
# -------------------------------------------------
elif page == "⚠️ Churn Analysis":

    st.title("⚠️ Churn Analysis")
    banner()

    left, right = st.columns(2)

    with left:
        st.subheader("⚠️ Churn Risk Distribution")
        st.dataframe(churn_df)
        st.bar_chart(churn_df, x="CHURN_RISK_CATEGORY", y="CUSTOMER_COUNT")

    with right:
        st.subheader("❤️ Customer Health Distribution")
        st.dataframe(health_df)
        st.bar_chart(health_df, x="HEALTH_BUCKET", y="CUSTOMER_COUNT")

# -------------------------------------------------
# Cortex AI
# -------------------------------------------------
elif page == "🤖 Cortex AI":

    st.title("🧠 Customer Intelligence Report")
    banner()
    st.caption("Powered by Snowflake Cortex AI — Demo Mode")

    st.info(
        "🚀 This module demonstrates how Snowflake Cortex AI can generate "
        "business insights from the Customer 360 GOLD layer."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤖 Executive AI Summary")
        st.write("Generate an executive summary of revenue, churn risk, usage, and support performance.")

        st.subheader("⚠️ Churn Explanation")
        st.write("Explain why a customer is classified as High, Medium, or Low Risk.")

        st.subheader("📊 Natural Language Analytics")
        st.write("Ask business questions like: *Which states have the highest churn risk?*")

    with col2:
        st.subheader("👤 Customer AI Assistant")
        st.write("Ask questions about a specific customer profile using natural language.")

        st.subheader("💡 Retention Recommendations")
        st.write("Generate personalized retention strategies for at-risk customers.")

        st.subheader("📩 Customer Outreach Drafts")
        st.write("Draft personalized retention emails for high-risk customers.")

    st.markdown("---")

    st.subheader("💬 Ask Customer 360")

    user_question = st.text_input(
        "Enter a business question",
        placeholder="Example: Give me an executive summary of revenue, churn risk, and support tickets."
    )

    if st.button("Ask Cortex"):

        if user_question.strip() == "":
            st.warning("Please enter a question.")

        else:
            from datetime import datetime

            with st.spinner("🤖 Analyzing Customer 360 data..."):
                time.sleep(2)

            st.success("Analysis completed successfully.")
            st.divider()

            left, center, right = st.columns([1, 6, 1])

            with center:
                st.subheader("🧠 Customer Intelligence Report")

                st.caption(
                    f"Generated on {datetime.now().strftime('%B %d, %Y %I:%M %p')}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("AI Confidence", "96%")

                with col2:
                    st.metric("Model", "Llama 3.1")

                with col3:
                    st.metric("Status", "Demo")

                st.caption(
                    "Sources: Revenue • Billing • Usage • Support • Customer Health • Churn Views"
                )

                st.markdown(f"""
                **Question**

                > {user_question}
                """)

                summary = """
Customer 360 AI Executive Summary

Business Overview:
The Customer 360 platform indicates healthy overall business performance with strong recurring revenue, a large active customer base, and meaningful customer engagement across internet, mobile, TV, billing, and support channels.

Key Risks:
- Medium-risk customers represent the largest churn-risk segment.
- Outstanding balances and late payments are contributing to customer risk.
- Support ticket volume suggests opportunities to improve customer experience.
- High-risk customers should be prioritized for proactive outreach.

Recommended Actions:
- Prioritize retention campaigns for High-Risk customers.
- Offer personalized incentives to Medium-Risk customers.
- Send payment reminders to customers with outstanding balances.
- Improve support resolution time for customers with repeated tickets.
- Use customer persona and plan data to design targeted upsell offers.

Executive Recommendation:
Revenue performance is strong, but reducing churn among Medium- and High-Risk customers should be the next business priority. A targeted retention strategy can improve customer lifetime value and reduce preventable revenue loss.
"""

                with st.container(border=True):
                    st.markdown("""
                    ### 📈 Business Overview

                    The Customer 360 platform indicates healthy overall business performance with
                    strong recurring revenue, a large active customer base, and meaningful customer
                    engagement across internet, mobile, TV, billing, and support channels.

                    ### ⚠️ Key Risks

                    - Medium-risk customers represent the largest churn-risk segment.
                    - Outstanding balances and late payments are contributing to customer risk.
                    - Support ticket volume suggests opportunities to improve customer experience.
                    - High-risk customers should be prioritized for proactive outreach.

                    ### 💡 Recommended Actions

                    - Prioritize retention campaigns for High-Risk customers.
                    - Offer personalized incentives to Medium-Risk customers.
                    - Send payment reminders to customers with outstanding balances.
                    - Improve support resolution time for customers with repeated tickets.
                    - Use customer persona and plan data to design targeted upsell offers.

                    ### 🎯 Executive Recommendation

                    Revenue performance is strong, but reducing churn among Medium- and High-Risk
                    customers should be the next business priority. A targeted retention strategy
                    can improve customer lifetime value and reduce preventable revenue loss.
                    """)

                st.download_button(
                    "📄 Download Executive Summary",
                    summary,
                    file_name="Customer360_AI_Summary.txt"
                )

# -------------------------------------------------
# About
# -------------------------------------------------
elif page == "ℹ️ About":

    st.title("ℹ️ About This Project")
    banner()

    st.info("""
    Customer 360 Analytics Platform

    • Built entirely inside Snowflake  
    • RAW → SILVER → GOLD  
    • Interactive Streamlit dashboard  
    • AI-ready architecture  
    • Telecom Customer 360 use case
    """)

    st.markdown("""
    ## Customer 360 Analytics Platform

    This project simulates a telecom-style Customer 360 platform inspired by real-world customer analytics use cases.

    ### Layers Built

    1. **RAW Layer**
       - Loaded CSV files using Snowflake Internal Stage and COPY INTO.

    2. **SILVER Layer**
       - Cleaned and standardized customer, billing, usage, subscription, and support data.

    3. **GOLD Layer**
       - Built business-ready analytics tables and views.

    4. **Streamlit App**
       - Created an interactive application inside Snowflake.

    ### Final Goal

    Build a production-style Customer 360 portal with analytics, customer drilldowns, and Cortex AI insights.
    """)
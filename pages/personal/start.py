import streamlit as st
import pandas as pd
import base64
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_base64_image(image_path):
    full_path = os.path.join(BASE_DIR, image_path)
    with open(full_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def getting_started():
    """Getting Started page"""

    # CSS
    st.markdown("""
    <style>
    * {
        font-family: Verdana, sans-serif !important;
    }
                
    .section-header {
        font-family: Verdana, sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: orange !important;
        margin-top: 2rem;
        margin-bottom: 1.2rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid orange;
    }
    
    .subsection-header {
        font-family: Verdana, sans-serif;
        color: #a4eba5 !important;
        font-size: 1.4rem;
        font-weight: 600;
        color: #4B5563;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    
    .text-content {
        font-family: Verdana, sans-serif;
        font-size: 1.1rem;
        color: white;
        line-height: 1.4;
        margin-bottom: 1rem;
    }
    
    .highlight-box {
        background-color: #94b8f2;
        border-left: 4px solid #164694;
        padding: 1rem;
        margin: 1.5rem 0;
        border-radius: 0.25rem;
    }
    
    .tip-box {
        background-color: #70b59e;
        border-left: 4px solid #0b543c;
        padding: 1rem;
        margin: 1.5rem 0;
        border-radius: 0.25rem;
    }
    
    .warning-box {
        background-color: #e0a4a4;
        border-left: 4px solid #EF4444;
        padding: 1rem;
        margin: 1.5rem 0;
        border-radius: 0.25rem;
    }
    
    .screenshot-container {
        margin: 1.5rem 0;
        text-align: center;
    }
    
    .screenshot-caption {
        font-family: Verdana, sans-serif;
        font-size: 0.9rem;
        color: #6B7280;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    .category-list {
        column-count: 2;
        column-gap: 2rem;
        margin: 1rem 0;
    }
    
    .category-item {
        margin-bottom: 0.5rem;
        break-inside: avoid;
    }
    
    .navigation-step {
        display: flex;
        align-items: center;
        margin-bottom: 0.8rem;
    }
    
    .step-number {
        display: inline-block;
        width: 1.8rem;
        height: 1.8rem;
        background-color: #3B82F6;
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 1.8rem;
        margin-right: 0.8rem;
        font-weight: bold;
    }
    
    .section-icon {
        margin-right: 0.5rem;
        color: #3B82F6;
    }
    
    .table-preview {
        width: 100%;
        border-collapse: collapse;
        margin: 1.5rem 0;
        font-size: 0.9rem;
    }
    
    .table-preview th {
        background-color: #30042a;
        padding: 0.5rem;
        text-align: left;
        border: 1px solid white;
    }
    
    .table-preview td {
        background-color: #3d2339;
        padding: 0.5rem;
        border: 1px solid white;
    }
                
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        gap: 8px;
        border-bottom: 2px solid #ba86aa;
    }
                
    .stTabs [data-baseweb="tab"] div {
        height: 50px;
        width: 380px;
        background-color: #ba86aa; 
        color: #2e0622;          
        border-radius: 8px 8px 0 0;
        padding: 10px;
        text-align: center;
        font-weight: bold !important;
        font-size: 18px !important;
        cursor: pointer;
    }
                
    .stTabs [aria-selected="true"] div {
        background-color: #6e2b5a; 
        color: white;           
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

    encoded_logo = get_base64_image("static/logo.png")

    with st.container():
        st.markdown(f"""
        <div style="background-color: #fffdd0; padding: 0px 10px 0px 60px; border-radius: 20px; width: 90%; margin-left: 20px; margin-bottom: 30px;">
            <div style="display: flex; align-items: center;">
                <div style="flex: 3;">
                    <h3 style="margin: 0; color: #1E1E1E;">Your Money, Sorted.<br>Smart Finance, Simplified.</h3>
                </div>
                <div style="flex: 1; text-align: right;">
                    <img src="data:image/png;base64,{encoded_logo}" alt="Finance App Logo" width="200">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <p class="text-content" style="margin-bottom: -10px;">
        Welcome to your personal finance management portal! PaisaVault is designed to help you track, analyze, 
        and optimize your financial activities with ease. This 'Getting Started' guide will walk you through 
        the different sections of the application and help you make the most of your financial data.
    </p>
    <div class="highlight-box">
        <center><p class="text-content" style="margin-bottom: 0; color: black">
            <strong>Your financial journey starts here!</strong> <br> This guide will help you navigate through all the 
            various features of PaisaVault.
        </p></center>
    </div>
    """, unsafe_allow_html=True)

    gsflow = get_base64_image("static/gsflow.PNG")
    st.markdown(f"""
    <div class="screenshot-container">
        <img src="data:image/png;base64,{gsflow}" alt="Upload Data Section" width="90%">
    </div>
    """, unsafe_allow_html=True)

    
    # Section 1: Upload Data
    st.markdown('<h3 class="section-header">1. Upload Data</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="text-content">
        This section allows you to upload your existing financial data from a CSV file or start 
        recording your transactions from scratch.
    </p>
    """, unsafe_allow_html=True)
    
    upload = get_base64_image("static/upload.PNG")
    st.markdown(f"""
    <div class="screenshot-container">
        <img src="data:image/png;base64,{upload}" alt="Upload Data Section" width="95%">
        <p class="screenshot-caption">Upload Data Section: Import your existing financial records</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h4 class="subsection-header">CSV File Format Requirements</h4>
    <p class="text-content">
        For seamless data integration, your CSV file should be formatted with these 6 columns:
    </p>
    """, unsafe_allow_html=True)
    
    # CSV Format Example
    csv_format = {
        'Column': ['Date', 'Mode', 'Category', 'Remark', 'Amount', 'Income_Expense'],
        'Format': ['dd-mm-yyyy', 'String', 'String', 'String', 'Numeric', 'String'],
        'Example': ['25-03-2025', 'Credit Card', 'Groceries', 'Weekly groceries', '2500', 'Expense']
    }
    
    csv_df = pd.DataFrame(csv_format)
    st.markdown(csv_df.to_html(index=False, classes='table-preview'), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tip-box" style="color: black;">
        <p class="text-content" style="color: black; margin-bottom: 0.5rem;"><strong>Tip:</strong> Using this exact format will ensure your data syncs correctly across the portal. You can also download a template CSV file to help you format your data correctly.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display additional details about the columns
    st.markdown("""
    <h4 class="subsection-header">Column Details</h4>
    
    <p class="text-content"><strong>Date:</strong> The date of the transaction in dd-mm-yyyy format.</p>
    
    <p class="text-content"><strong>Mode:</strong> The payment method used for the transaction. Valid options include - Cash, Credit Card, Debit Card, UPI, Bank Transfer, Cheque, Mobile Wallet, Automatic Payment, Net Banking, Other</p>
    
    <p class="text-content"><strong>Category:</strong> Classification of the transaction. Valid categories include - Rent, Groceries, Healthcare, Transportation, Utilities, Communication, Education, Enrichment, Domestic Help, Care Essentials, Financial Dues, Discretionary, Salary, Side Hustle, Pension, Interest, Rewards, Stocks, Gifts, Miscellaneous</p>

    <p class="text-content"><strong>Remark:</strong> A brief note about the transaction (2-5 words recommended).</p>
    
    <p class="text-content"><strong>Amount:</strong> The monetary value of the transaction.</p>
    
    <p class="text-content"><strong>Income_Expense:</strong> Type of transaction - either "Income" or "Expense".</p>
        """, unsafe_allow_html=True)
    
    # What happens after upload
    st.markdown("""
    <h4 class="subsection-header">After Upload</h4>
    <p class="text-content">
        Once you upload your CSV file, you'll see a summary and preview of your transaction table.
        From here, you can:
    </p>
    <ul>
        <li>Review your imported transactions</li>
        <li>Edit or delete individual transactions</li>
        <li>Save your changes</li>
        <li>Export your updated data as a downloadable file</li>
    </ul>
    
    <div class="warning-box">
        <p class="text-content" style="margin-bottom: 0; color: black;">
            <strong>Important:</strong> If you don't have existing data, you can skip this step and go directly to the 
            "Income/Expense" section to start recording your transactions from scratch.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 2: Overview
    st.markdown('<h3 class="section-header">2. Overview</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="text-content">
        The Overview section provides a comprehensive summary of your financial activity with 
        visual representations to help you understand your spending and income patterns.
    </p>
    """, unsafe_allow_html=True)
    
    overview = get_base64_image("static/overview.PNG")
    st.markdown(f"""
    <div class="screenshot-container">
        <img src="data:image/png;base64,{overview}" alt="Overview Dashboard" width="100%">
        <p class="screenshot-caption">Overview Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p class="text-content">
        In this section, you'll find:
    </p>
    <ul>
        <li>Pie charts showing expense and income distribution by category</li>
        <li>Line charts displaying financial trends over time</li>
        <li>Total savings calculations for your selected time period</li>
        <li>Highlights and key metrics for the current month</li>
    </ul>
    
    <div class="tip-box">
        <p class="text-content" style="margin-bottom: 0; color: black">
            <strong>Tip:</strong> Use the time period selector to view your financial data for specific 
            timeframes, such as the last month, quarter, or year.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 3: Income/Expense
    st.markdown('<h3 class="section-header">3. Income/Expense</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="text-content">
        This is where you can add new transactions to your financial records. The section is designed to make 
        recording your daily expenses and income sources quick and intuitive.
    </p>
    """, unsafe_allow_html=True)
    
    record = get_base64_image("static/record.PNG")
    st.markdown(f"""
    <div class="screenshot-container">
        <img src="data:image/png;base64,{record}" alt="Income/Expense Section" width="90%">
        <p class="screenshot-caption">Income/Expense Section: Easily record new transactions</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h4 class="subsection-header">How to Add a New Transaction</h4>
    
    <div class="navigation-step">
        <span class="step-number">1</span>
        <span>Click on the category icon that matches your transaction</span>
    </div>
    <div class="navigation-step">
        <span class="step-number">2</span>
        <span>Fill in the transaction details in the form that appears</span>
    </div>
    <div class="navigation-step">
        <span class="step-number">3</span>
        <span>Select the payment mode, amount, add a brief remark, and choose the date</span>
    </div>
    <div class="navigation-step">
        <span class="step-number">4</span>
        <span>Click Save to add the transaction to your records</span>
    </div>
    <div class="navigation-step">
        <span class="step-number">5</span>
        <span>To view your updated transactions, navigate to the Upload Data section</span>
    </div>
    
    <p class="text-content">
        The category will be automatically recorded based on the icon you selected. 
        This section also displays your 5 most recent transactions for quick reference.
    </p>
    
    <div class="tip-box">
        <p class="text-content" style="margin-bottom: 0; color: black">
            <strong>Tip:</strong> Clicking on any category will show you examples of expenses that fall under that classification, 
            helping you categorize your transactions correctly.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 4: Financial Foresight
    st.markdown('<h3 class="section-header">4. Financial Foresight</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="text-content">
        The Financial Foresight section offers predictive tools to help you plan your financial future. 
        This section has two powerful subsections:
    </p>
    <ul>
        <li><strong>Butterfly Effect Simulator</strong></li>
        <li><strong>Financial Scenario Tester</strong></li>
    </ul>
    """, unsafe_allow_html=True)

    
    def butterfly_effect_description():
        st.markdown("""
        <h3 style="color: orange; font-weight: bold;">
            Butterfly Effect Simulator
        </h3>
        
        <p class="text-content">
        The Butterfly Effect Simulator demonstrates how minor financial decisions today can create dramatic impacts on your future wealth over time.
        </p>
                    
        <h4 style="color: #a4eba5; font-weight: bold;">
            What is the Butterfly Effect?
        </h4>
        <p class="text-content">
        In chaos theory, the butterfly effect illustrates how small initial changes in complex systems can lead to significantly different outcomes over time. In finance, this concept applies to how seemingly insignificant daily financial decisions compound dramatically over years.
        </p>
        
        <h4 style="color: #a4eba5; font-weight: bold;">
            Real-Life Examples of the Butterfly Effect in Finance
        </h4>
        <ol>
            <li>
                <strong>The Starbucks Coffee Example</strong> - Suppose you buy a ₹260 Starbucks coffee every day. That's ₹7,800 a month and ₹94,900 a year. If you invested that money instead, with a modest annual return of 7%, you could accumulate over ₹14 lakh in ten years! A simple decision to skip daily coffee could significantly impact your long-term financial health.
            </li>
            <br>
            <li>
                <strong>Starting to Save Early</strong> - If two people, Rahul and Aditya, both decide to invest for retirement, but Rahul starts investing ₹8,000 a month at age 25, while Aditya starts at 35, Rahul will have significantly more wealth at retirement due to the power of compound interest, even if they both stop investing at 60.
            </li>
        </ol>
        
        <h4 style="color: #a4eba5; font-weight: bold;">
            How to use the simulator?
        </h4>
        <p class="text-content">
        <ul>
            <li>Enter your financial details, including income, expenses, and savings.</li>
            <li>Adjust different parameters to see how small financial changes impact your future.</li>
            <li>Get insights on whether your financial habits are leading towards stability, growth, or risk.</li>
        </ul>
        </p>
        """, unsafe_allow_html=True)
     
    def financial_scenario_description():
        st.markdown("""
        <h3 style="color: orange; font-weight: bold;">
            Financial Scenario Tester
        </h3>
        
        <p class="text-content">
        Plan, Assess, and Secure Your Future. Managing personal finances effectively requires more than just tracking income and expenses—it's about preparing for uncertainties, assessing financial resilience, and setting achievable goals.
        </p>
        
        <h4 style="color: #a4eba5; font-weight: bold;">
           How does it work?
        </h4>
        <p class="text-content">
        The Financial Scenario Tester takes into account key personal and financial details, including age, number of dependents, income and monthly expenses. Using this data, the model calculates: Savings projection, Net worth, Survival duration in case of emergency, Future spend patterns, Goal achievability scores.
        </p>
        
        <h4 style="color: #a4eba5; font-weight: bold;">
            Key Features
        </h4>
        <ul>
            <li>
                <strong>Economic Habit Score</strong> – Evaluates spending and saving habits to give users a financial health rating.
            </li>
            <li>
                <strong>Personalized Advice</strong> – Offers recommendations to improve financial discipline, such as better budgeting strategies, expense reduction techniques, and investment opportunities.
            </li>
            <li>
                <strong>Asset Allocation Overview</strong> – Displays how your wealth is distributed across savings, investments, and liabilities, providing insights into diversification and risk exposure.
            </li>
            <li>
                <strong>Resilience Score</strong> – Assesses financial preparedness and classifies users into categories such as:
                <ul>
                    <li><strong>Good: </strong>Well-prepared with a strong financial cushion.</li>
                    <li><strong>Moderate: </strong>Stable but needs improvement in savings or investment strategies.</li>
                    <li><strong>Warning: </strong>At risk, requiring immediate action to improve financial stability.</li>
                </ul>
            </li>
        </ul>
        
        """, unsafe_allow_html=True)
        
    tab1, tab2 = st.tabs(["Butterfly Effect Simulator", "Financial Scenario Tester"])
    
    with tab1:
        butterfly_effect_description()
    
    with tab2:
        financial_scenario_description()
    
    # Section 5: Custom Bot
    st.markdown('<h3 class="section-header">5. Custom Bot</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="text-content">
        The Custom Bot is your personal financial assistant, trained on your specific financial data 
        to provide tailored insights and answers to your questions.
    </p>
    """, unsafe_allow_html=True)
    
    custom = get_base64_image("static/chat.PNG")
    st.markdown(f"""
    <div class="screenshot-container">
        <img src="data:image/png;base64,{custom}" alt="Custom Bot Interface" width="100%">
        <p class="screenshot-caption">Custom Bot: Your personal financial assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <h4 class="subsection-header">Two Specialized Assistants</h4>
    
    <p class="text-content">
        <strong>DataDigger:</strong> Answers transactional queries about your spending and income patterns.
    </p>
    <p class="text-content">Examples of questions you can ask DataDigger:</p>
    <ul>
        <li>"What did I spend most on last month?"</li>
        <li>"Which is my lowest spend category?"</li>
        <li>"What is my biggest income source?"</li>
        <li>"How much have I saved in the last 6 months?"</li>
        <li>"How much did I spend yesterday on shopping?"</li>
    </ul>
    
    <div class="warning-box">
        <p class="text-content" style="margin-bottom: 0; color: black">
            <strong>Important:</strong> For accurate answers, always mention specific column names or categories within quotes. 
            For example, ask "How much did I spend on "Groceries" last month?" instead of 
            "How much did I spend on groceries last month?"
        </p>
    </div>
    
    <p class="text-content">
        <strong>FinMentor:</strong> Provides financial advice and insights based on your data.
    </p>
    <p class="text-content">Examples of questions you can ask FinMentor:</p>
    <ul>
        <li>"How can I improve my savings to buy a car in 3 years?"</li>
        <li>"How can I improve my spending habits by using the butterfly effect simulator?"</li>
        <li>"How can I test my financial stability by using the scenario tester?"</li>
        <li>"What areas should I cut back on to increase my monthly savings?"</li>
        <li>"How does my spending compare to recommended financial guidelines?"</li>
    </ul>
    """, unsafe_allow_html=True)
    
    # Section 6: Explore Resources
    st.markdown('<h3 class="section-header">6. Explore Resources</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="text-content">
        The Explore Resources section provides access to educational materials and tools to 
        enhance your financial literacy and decision-making skills.
    </p>
    
    <p class="text-content">
        Browse through curated articles, videos and guides covering various aspects of 
        personal finance, like - Budgeting strategies, Retirement preparation, Financial Leverage, Investment fundamentals, Financial Instruments and much more!
    </p>
    
    <div class="tip-box">
        <p class="text-content" style="margin-bottom: 0; color: black;">
            <strong>Tip:</strong> Check out this section for new topics to add to your existing knowledge base.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section 7: Log Out
    st.markdown('<h3 class="section-header">7. Log Out</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="text-content">
        When you're finished using PaisaVault, click the Log Out button to securely exit your account.
        This will return you to the general landing page of the application.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight-box">
        <center><h3 style="margin-top: 0; color: #1E3A8A; font-size: 1.3rem;">Ready to Take Control of Your Finances?</h3>
        <p class="text-content" style="margin-bottom: 0; color: #1E3A8A">
            Now that you're familiar with PaisaVault's features, feel free to explore the application. 
            Begin by uploading your existing data or recording your first transaction!
        </p></center>
    </div>
    """, unsafe_allow_html=True)
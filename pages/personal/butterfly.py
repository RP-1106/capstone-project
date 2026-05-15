import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime
import random

def get_monthly_averages(df):
    """Calculate average monthly expenses and income by category"""
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    
    df['Month_Year'] = df['Date'].dt.to_period('M')
    
    # Get number of unique months in the data
    num_months = df['Month_Year'].nunique()
    if num_months == 0:
        num_months = 1  # Avoid division by zero
    
    # Calculate monthly average for each category
    monthly_avg = {}
    
    # Group by category and calculate monthly average
    category_sums = df.groupby(['Category', 'Income_Expense'])['Amount'].sum()
    
    for (category, income_expense), total_amount in category_sums.items():
        monthly_avg[category] = total_amount / num_months
    
    return monthly_avg

def generate_projection(base_value, months, variance=0.6):
    """Generate projections with saving trends"""
    projection = []
    current_value = base_value
    
    for i in range(months):
        # More pronounced seasonality for certain months
        seasonal_factor = 1.0
        month_num = (datetime.datetime.now().month + i) % 12
        
        # Higher spending in November-December, lower in January-February
        if month_num in [10, 11]:  # November, December
            seasonal_factor = 1.1
        elif month_num in [0, 1]:  # January, February
            seasonal_factor = 0.9
        
        # Random fluctuation
        fluctuation = random.uniform(1 - variance, 1 + variance)
        
        # Combine base trend with seasonal factor and random fluctuation
        current_value = base_value * seasonal_factor * fluctuation
        projection.append(current_value)
    
    return projection

def calculate_savings(df, monthly_expenses, category_adjustments, months_to_predict):
    """Calculate current and projected savings"""
    # Calculate total monthly income and expenses
    monthly_income = sum(amount for category, amount in monthly_expenses.items() 
                        if category in df[df['Income_Expense'] == 'Income']['Category'].unique())
    
    monthly_expense = sum(amount for category, amount in monthly_expenses.items() 
                         if category in df[df['Income_Expense'] == 'Expense']['Category'].unique())
    
    # Calculate reduced expenses based on adjustments
    reduced_expenses = {}
    for category, reduction_pct in category_adjustments.items():
        if category in monthly_expenses:
            original_amount = monthly_expenses[category]
            reduced_expenses[category] = original_amount * (1 - reduction_pct / 100)
        else:
            reduced_expenses[category] = 0
    
    # Calculate total reduced monthly expense
    adjusted_monthly_expense = monthly_expense
    for category, adjustment in category_adjustments.items():
        if category in monthly_expenses:
            savings = monthly_expenses[category] * (adjustment / 100)
            adjusted_monthly_expense -= savings
    
    # Current monthly savings
    current_monthly_savings = monthly_income - monthly_expense
    
    # Projected monthly savings
    projected_monthly_savings = monthly_income - adjusted_monthly_expense
    
    # Generate projections
    current_savings_projection = generate_projection(current_monthly_savings, months_to_predict)
    projected_savings_projection = generate_projection(projected_monthly_savings, months_to_predict)
    
    # Calculate cumulative savings
    total_current_savings = sum(current_savings_projection)
    total_projected_savings = sum(projected_savings_projection)
    
    return current_savings_projection, projected_savings_projection, total_current_savings, total_projected_savings

def display_savings_graph(current_monthly_savings, projected_monthly_savings, months_to_predict):
    """Display the savings projection graph"""
    st.markdown("<center><h3>Savings Projection</h3></center>", unsafe_allow_html=True)
    
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    
    months = []
    for i in range(months_to_predict):
        month_num = (current_month + i - 1) % 12 + 1
        year = current_year + (current_month + i - 1) // 12
        month_name = datetime.date(1900, month_num, 1).strftime('%b')
        months.append(f"{month_name} {year}")
    
    # Calculate cumulative savings
    cumulative_current = np.cumsum(current_monthly_savings)
    cumulative_projected = np.cumsum(projected_monthly_savings)
    
    fig = go.Figure()
    
    # Add current savings trend
    fig.add_trace(go.Scatter(
        x=months,
        y=cumulative_current,
        mode='lines',
        name='Current',
        line=dict(color='#cf9d4c', width=2, dash='dash', shape='spline')
    ))
    
    # Add projected savings trend
    fig.add_trace(go.Scatter(
        x=months,
        y=cumulative_projected,
        mode='lines',
        name='Projected',
        line=dict(color='#38a67d', width=2, shape='spline')
    ))

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Cumulative Savings (₹)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add monthly savings comparison
    st.markdown(
        f"""
        <div style='text-align: center; margin-top: -30px;'>
            <p>Average Monthly Savings: <br>
               <span style='color: #cf9d4c;'><b>Current: ₹{sum(current_monthly_savings)/months_to_predict:.2f}</b></span> vs 
               <span style='color: #38a67d;'><b>Projected: ₹{sum(projected_monthly_savings)/months_to_predict:.2f}</b></span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_sankey_chart(df, category_adjustments, monthly_expenses):
    """Display Sankey chart showing income and expense flows with distinct colors for categories"""
    # Get income and expense categories
    income_categories = df[df['Income_Expense'] == 'Income']['Category'].unique()
    expense_categories = df[df['Income_Expense'] == 'Expense']['Category'].unique()
    
    # Calculate total monthly income
    total_monthly_income = sum(monthly_expenses.get(category, 0) 
                              for category in income_categories)
    
    # Prepare nodes and links for Sankey diagram
    label_list = ['Total Income'] + list(income_categories) + ['Total Expenses'] + list(expense_categories)
    
    # Map category names to indices
    category_to_index = {category: i+1 for i, category in enumerate(income_categories)}
    category_to_index.update({category: i+2+len(income_categories) for i, category in enumerate(expense_categories)})
    
    # Generate color palettes
    income_colors = px.colors.sample_colorscale("Greens", len(income_categories))[::-1]
    expense_colors = px.colors.sample_colorscale("Reds", len(expense_categories))[::-1]
    
    # Create node colors
    node_colors = ['rgba(44, 160, 44, 0.8)']  # Total Income in green
    node_colors.extend([color for color in income_colors]) 
    node_colors.append('rgba(214, 39, 40, 0.8)')  # Total Expenses in red
    node_colors.extend([color for color in expense_colors])
    
    links = []
    
    for i, category in enumerate(income_categories):
        if category in monthly_expenses:
            links.append({
                'source': category_to_index[category],
                'target': 0,
                'value': monthly_expenses[category],
                'color': income_colors[i]
            })
    
    # Total Income to Total Expenses
    links.append({
        'source': 0,  # Total Income
        'target': 1 + len(income_categories),  # Total Expenses
        'value': total_monthly_income,
        'color': 'rgba(150, 150, 150, 0.3)'  # Neutral color for the main flow
    })
    
    for i, category in enumerate(expense_categories):
        if category in monthly_expenses:
            if category in category_adjustments:
                value = monthly_expenses[category] * (1 - category_adjustments[category] / 100)
            else:
                value = monthly_expenses[category]
            
            links.append({
                'source': 1 + len(income_categories),  # Total Expenses
                'target': category_to_index[category],
                'value': value,
                'color': expense_colors[i]
            })
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=label_list,
            color=node_colors
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
            color=[link['color'] for link in links]
        )
    )])
    
    fig.update_layout(
        font_size=10,
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_recommendations(df, category_adjustments):
    """Display personalized recommendations based on spending habits and adjustments"""
    # Convert adjustments to list of tuples (category, pct) and sort by pct
    sorted_adjustments = sorted(
        [(category, adj) for category, adj in category_adjustments.items() if adj > 0],
        key=lambda x: x[1],
        reverse=True
    )
    
    # Generate personalized recommendations
    recommendations = []
    
    # Specific recommendations based on category adjustments
    for category, adjustment in sorted_adjustments:
        if category == 'Discretionary' and adjustment >= 10:
            recommendations.append({
                'title': 'Smart Discretionary Spending',
                'content': f"You're reducing discretionary spending by {adjustment}%. Try the 24-hour rule: wait 24 hours before any non-essential purchase to avoid impulse buying."
            })
        
        elif category == 'Groceries' and adjustment >= 10:
            recommendations.append({
                'title': 'Grocery Shopping Strategy',
                'content': f"For your {adjustment}% grocery reduction, try meal planning, buying in bulk, and using homemade alternatives to processed products or store-specific apps for additional savings."
            })
        
        elif category == 'Transportation' and adjustment >= 15:
            recommendations.append({
                'title': 'Transportation Alternatives',
                'content': f"To achieve your {adjustment}% transportation savings, consider carpooling, public transit, or cycling for shorter trips."
            })
        
        elif category == 'Utilities' and adjustment >= 10:
            recommendations.append({
                'title': 'Energy Efficiency',
                'content': f"For your {adjustment}% utilities reduction goal, go for LED lighting, energy-efficient appliances and don't forget to switch off the lights and fans carelessly if your are not using the room!"
            })
        
        elif category == 'Communication' and adjustment >= 15:
            recommendations.append({
                'title': 'Communication Cost-Cutting',
                'content': f"To reduce communication expenses by {adjustment}%, review your phone and internet plans for unused services. Consider bundle discounts or family plans for additional savings."
            })
        
        elif category == 'Domestic Help' and adjustment >= 20:
            recommendations.append({
                'title': 'Domestic Help Alternatives',
                'content': f"For your {adjustment}% reduction in domestic help, try to do some household chores on your own and consider task-sharing with family members, instead of overly relying on domestic workers for day-to-day things."
            })
        
        elif category == 'Rent' and adjustment >= 5:
            recommendations.append({
                'title': 'Housing Cost Management',
                'content': f"Your {adjustment}% rent reduction goal is significant. Consider negotiating with your landlord, finding a roommate, or exploring less expensive neighborhoods enough to suffice your needs."
            })
    
    if recommendations:
        for rec in recommendations:
            st.markdown(f"""
            <div style='background-color:#2d2d2d; border-left:4px solid #4e807c; 
                        border-radius:6px; padding:12px 16px; margin-bottom:10px;'>
                <strong style='color:#78c4be;'>{rec['title']}</strong>
                <p style='margin-top:8px; margin-bottom:0; color:white;'>{rec['content']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Generic advice
    st.markdown("<h3 style='margin-top: 20px; margin-bottom: -25px'>General Financial Advice</h3>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='highlight-card' style='line-height: 1.3; background-color: #63bdeb; color: #14384a; border-left:5px solid #1a5775; margin-bottom: 30px;'>
            <h4>The Power of Small Changes</h4>
            <p>Remember the butterfly effect: Small, consistent changes in your spending habits can lead to dramatically different financial outcomes over time. The compounding effect of these savings, especially when invested, can significantly impact your long-term financial health.</p>
            <h4>Follow the 50/30/20 Rule</h4>
            <p>A healthy budget typically allocates:</p>
            <ul>
                <li>50% of income to needs (housing, groceries, utilities)</li>
                <li>30% to wants (entertainment, dining out)</li>
                <li>20% to savings and debt repayment</li>
            </ul>
            <h4>Pay Yourself First</h4>
            <p>Set up automatic transfers to your savings account on payday before spending on discretionary items. This habit ensures consistent progress toward your financial goals.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def butterfly():
    """Butterfly Effect Simulator"""

    # CSS
    st.markdown("""
    <style>
        * {
            font-family: Verdana, sans-serif !important;
        }
        .highlight-card {
            background-color: #d1796f;
            border-radius: 10px;
            border-left:5px solid #591810;
            padding: 20px;
            color: #3b0d07;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .recommendation-card {
            background-color: #a442f5;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 5px solid #1f77b4;
        }
        .savings-positive {
            color: #033d1a;
            font-weight: bold;
        }
        .section-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.write("## 🦋 Butterfly Effect Simulator")

    st.markdown("""
    <div style="background-color:#7fc9ab; color: #13241d; padding: 5px 10px 1px 10px; margin-bottom: 30px; border-radius:10px; border-left:5px solid #2a805d">
        <center><h3>A Chaos Theory concept in Personal Finance!</h3>
        <p>Explore how small changes in your spending habits can lead to significant financial outcomes over time. Adjust the sliders to see the projected impact on your savings.</p></center>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'finance_df' not in st.session_state:
        st.session_state.finance_df = None
    
    if st.session_state.finance_df is None:
        st.warning("Please upload data first, record some transactions or use the sample dataset.")
        if st.button("⬅ Back to Dashboard"):
            st.session_state.menu_state = "main"
            st.rerun()
    else:
        df = st.session_state.finance_df.copy()
        
        if not pd.api.types.is_datetime64_any_dtype(df['Date']):
            df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        
        monthly_expenses = get_monthly_averages(df)
        
        st.sidebar.markdown("## Grow your Savings!")
        
        # Time range selection for predictions
        prediction_periods = {
            "3 Months": 3,
            "6 Months": 6,
            "12 Months": 12
        }
        
        prediction_period = st.sidebar.selectbox(
            "Select Prediction Time Range:",
            list(prediction_periods.keys()),
            index=1  # Default to 6 months
        )
        
        months_to_predict = prediction_periods[prediction_period]
        
        # Categories to adjust
        adjustable_categories = ['Discretionary', 'Groceries', 'Transportation', 
                                'Utilities', 'Communication', 'Domestic Help', 'Rent']
        
        # Create sliders for each adjustable category
        st.sidebar.markdown(f"""
            <div style='margin-top: 20px; margin-bottom: 20px; font-size: 20px;'>
                <strong>Expense Reduction</strong><br>
                <span style = 'font-size: 13px'>(PMA: Present Monthly Average)</span>
            </div>
        """, unsafe_allow_html=True)
        category_adjustments = {}
        
        for category in adjustable_categories:
            current_monthly = monthly_expenses.get(category, 0)
            if current_monthly > 0:
                st.sidebar.markdown(f"""
                    <div style='margin-bottom: -10px'>
                        <strong>{category}</strong><br>
                        <span style = 'font-size: 13px'>(PMA: ₹{current_monthly:.2f}/month)</span>
                    </div>
                """, unsafe_allow_html=True)
                category_adjustments[category] = st.sidebar.slider(
                    f"Reduce {category} by:",
                    min_value=0, 
                    max_value=50,  
                    value=10,      
                    step=1,
                    format="%d%%",
                    key=f"slider_{category}"
                )
            else:
                category_adjustments[category] = 0
                
        # Calculate current and projected savings
        current_monthly_savings, projected_monthly_savings, total_current_savings, total_projected_savings = calculate_savings(
            df, monthly_expenses, category_adjustments, months_to_predict
        )
        
        col1, col2 = st.columns([1, 2])
        
        # Highlights
        with col1:
            st.markdown("<center><h3>Highlights</h3></center>", unsafe_allow_html=True)
        
            # Calculate savings difference
            savings_difference = total_projected_savings - total_current_savings
            
            # Display total projected savings
            st.markdown(
                f"""
                <div class='highlight-card'>
                    <center><h4>Total Potential Savings</h4></center>
                    <p style='margin-bottom: -10px;'>Over the next {months_to_predict} months:</p>
                    <h3>₹{total_projected_savings:.2f}</h3>
                    <p style='margin-top: 20px'>That's <span class='savings-positive'>₹{savings_difference:.2f} more</span> than your current trend!</p>
                    <p>Monthly average savings increase: <span class='savings-positive'>₹{savings_difference/months_to_predict:.2f}</span></p>
                </div>
                """, 
                unsafe_allow_html=True
            )

        # Projected Savings Graph
        with col2:
            display_savings_graph(current_monthly_savings, projected_monthly_savings, months_to_predict)

        st.markdown("<h3 style='margin-bottom: -45px'>So, what did we find?</h3>", unsafe_allow_html=True)

        h1, h2 = st.columns([1,1])
        with h1:
        # Display most impactful changes
            sorted_adjustments = sorted(
                [(category, adj) for category, adj in category_adjustments.items() if adj > 0],
                key=lambda x: x[1],
                reverse=True
            )
            
            if sorted_adjustments:
                st.markdown(
                    f"""
                    <div class='highlight-card' style='padding: 10px 10px 1px 15px; background-color: #a986d1; border-left:5px solid #583680; color: #2c1547; margin-top: 20px;'>
                        <center><h4>Your Most Impactful Changes</h4></center>
                        <ul>
                            {"".join(f"<li>Reducing <b>{category}</b> by {adj}%</li>" for category, adj in sorted_adjustments[:3])}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        with h2:
            # Display potential uses for savings
            potential_uses = []
            if savings_difference > 5000:
                potential_uses.append("Start an emergency fund")
            if savings_difference > 2500:
                potential_uses.append("Pay down high-interest debt")
            if savings_difference > 1000:
                potential_uses.append("Save for a vacation")
            
            if potential_uses:
                st.markdown(
                    f"""
                    <div class='highlight-card' style='padding: 10px 10px 1px 15px; background-color: #f5ec76; color: #8c2f04; border-left:5px solid #b35305; margin-top: 20px;'>
                        <center><h4>What You Could Do With These Savings</h4></center>
                        <ul>
                            {"".join(f"<li>{use}</li>" for use in potential_uses)}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        
        # Sankey chart
        st.markdown("<h3 style='margin-top: 30px; margin-bottom: -100px'>Monthly Income & Expense Flow<h3>", unsafe_allow_html=True)
        display_sankey_chart(df, category_adjustments, monthly_expenses)
        
        # Recommendations
        st.markdown("<h3 style='margin-bottom: -25px'>Personalized Recommendations</h3>", unsafe_allow_html=True)

        display_recommendations(df, category_adjustments)

        if st.button("⬅ Back to Dashboard"):
            st.session_state.menu_state = "main"
            st.rerun()
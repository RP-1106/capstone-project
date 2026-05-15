import streamlit as st

def features_page():
    """Features section highlighting the app's unique capabilities"""
    
    # CSS
    st.markdown("""
    <style>
    * {
        font-family: Verdana, sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: -20px; margin-top: -10px">
      <h3 style="margin: 0;">What new do we offer?</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <p style="font-size: 18px; margin-bottom: 30px;">
      Explore how PaisaVault helps you in personal finance management with these innovative features.
    </p>
    """, unsafe_allow_html=True)
    
    # Feature 1: AI Chatbot
    st.markdown("""
    <div style="background-color: #D3D3D3; border-radius: 30px; padding: 15px; margin-bottom: 30px; border-left: 5px solid #055d13;">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
            <h3 style="margin: 0; color: #055d13;">📱 Personalized AI Assistant</h3>
            <div style="flex-grow: 1; height: 2px; background-color: #055d13;"></div>
        </div>
        <div style="margin: 10px 0; color: #373938;">
            <p>Your financial advisor that understands <i>you</i>. Our AI chatbot learns from your transaction history, spending categories, and financial goals to provide tailored guidance.</p>
            <ul>
                <li><b>Ask anything</b>: "How can I save more on groceries?" or "Suggest a savings plan for my vacation next year"</li>
                <li><b>Custom insights</b>: Receive personalized recommendations based on your unique spending patterns</li>
                <li><b>Goal tracking</b>: Get real-time updates on your progress toward financial targets</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("static/chat.png", caption="AI Assistant Dashboard", use_container_width=True)
    
    # Feature 2: Butterfly Effect Model
    st.markdown("""
    <div style="background-color: #D3D3D3; border-radius: 30px; padding: 15px; margin: 30px 0; border-left: 5px solid #0b52a8;">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
            <h3 style="margin: 0; color: #0b52a8;">🦋 Butterfly Effect Model</h3>
            <div style="flex-grow: 1; height: 2px; background-color: #0b52a8;"></div>
        </div>
        <div style="margin: 20px 0; color: #373938;">
            <p>See how small financial decisions today can create profound changes in your future. Our neural networks and LSTM models analyze your discretionary spending patterns to reveal surprising long-term outcomes.</p>
            <ul>
                <li><b>Visual compound effects</b>: Watch how small savings grow exponentially over time</li>
                <li><b>Chaos Theory</b>: Understand how choas theory works in real life with your money</li>
                <li><b>Pattern recognition</b>: Identify spending habits you never knew were affecting your financial health</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("static/butterfly.jpg", caption="Butterfly Effect Dashboard", use_container_width=True)
    
    # Feature 3: Scenario Testing Model
    st.markdown("""
    <div style="background-color: #d3d3d3; border-radius: 30px; padding: 15px; margin: 30px 0; border-left: 5px solid #bd1a49;">
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
            <h3 style="margin: 0; color: #bd1a49;">🔮 Scenario Testing Model</h3>
            <div style="flex-grow: 1; height: 2px; background-color: #bd1a49;"></div>
        </div>
        <div style="margin: 20px 0; color: #373938;">
            <p>Our breakthrough in financial forecasting combines machine learning with Monte Carlo simulations for unparalleled predictive accuracy across multiple time horizons.</p>
            <ul>
                <li><b>Probability mapping</b>: Understand the exact likelihood of achieving your financial goals</li>
                <li><b>Stress testing</b>: See how your finances would perform under various economic conditions</li>
                <li><b>Goal calibration</b>: Adjust your targets based on data-driven success probabilities</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("static/car.JPG", caption="Scenario Testing Dashboard", use_container_width=True)
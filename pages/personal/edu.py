import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import base64

def education():

   # CSS
   st.markdown("""
   <style>
   * {
      font-family: Verdana, sans-serif !important;
   }
   </style>
   """, unsafe_allow_html=True)

   st.write("## 🧭 Explore Resources")
   st.write("Access insightful articles, videos to boost your financial IQ & make smarter money moves.")

   def img_to_b64(path):
      """Function to encode PNG image to base64"""
      with open(path, "rb") as image_file:
         encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
      return f"data:image/png;base64,{encoded_string}"

   def centered_link_button(col, label, image_path, link, key):
      b64_image = img_to_b64(image_path)
      if "video.png" in image_path:
         bg_color = "#f08080 "
      elif "bill.png" in image_path:
         bg_color = "#CC99CC"
      else:
         bg_color = "#f0f0f0"

      with stylable_container(
         key=key + "_container",
         css_styles=f"""
               .button-wrapper {{
                  width: 200px;
                  height: 175px;
                  display: flex;
                  flex-direction: column;
                  align-items: center;
                  justify-content: center;
                  border-radius: 20px;
                  background-color: {bg_color};  /* Dynamic background color */
                  margin: 8px;
                  padding: 10px;
               }}
               .button-wrapper a {{
                  display: flex;
                  flex-direction: column;
                  align-items: center;
                  justify-content: center;
                  text-decoration: none;
                  color: inherit;
               }}
               .button-wrapper img {{
                  width: 50%; /* Smaller icon (was 80%) */
                  height: auto;
                  object-fit: contain;
                  margin-bottom: 5px;
               }}
               .button-wrapper span {{
                  font-size: 1.2em; /* Larger label (adjust as needed) */
                  font-weight: bold; /* Bold label */
                  text-align: center;
                  color: black;
                  
               }}
         """,
      ):
         st.markdown(f"""<div class="button-wrapper">
               <a href="{link}" target="_blank">
                  <img src="{b64_image}">
                  <span>{label}</span>
               </a>
         </div>""", unsafe_allow_html=True)
         if st.session_state.get(key):
               st.write(f"{label} button clicked!")
               del st.session_state[key]

   one, two, left, middle, right, six, seven = st.columns([1, 1, 7, 7, 7, 1, 1])

   button_data = {
      left: [
         ("What is Finance", "static/bill.png", "https://corporatefinanceinstitute.com/resources/wealth-management/what-is-finance-definition/?utm_source=morning_brew", "learn1_button"),  # Added link
         ("Fin-Instruments", "static/bill.png", "https://marketbusinessnews.com/financial-glossary/financial-instrument/?utm_source=morning_brew", "learn2_button"),  # Added link
         ("Finance for Dummies", "static/video.png", "https://www.youtube.com/watch?v=DNYCgsyOAW4", "learn7_button"),  # Added link
      ],
      middle: [
         ("Financial Leverage", "static/video.png", "https://www.youtube.com/watch?v=7suzYQOh4VA", "learn3_button"),  # Added link
         ("Equity vs Debt", "static/bill.png", "https://www.business.com/articles/debt-vs-equity-financing/", "learn4_button"),  # Added link
         ("Saving for Retirement", "static/medium.png", "https://medium.com/fintechexplained/invest-early-and-retire-early-for-financial-independence-b635b315697a", "learn8_button"),  # Added link
      ],
      right: [
         ("Risk vs Reward Ratio", "static/video.png", "https://www.youtube.com/watch?v=aKZsireNBIM", "learn5_button"),  # Added link
         ("Mutual Funds", "static/bill.png", "https://money.usnews.com/investing/funds/articles/best-guide-to-mutual-funds?utm_source=morning_brew", "learn6_button"),  # Added link
         ("Beginners Ultimate Guide", "static/medium.png", "https://medium.com/@rishabhshah330/basics-of-finance-beginners-ultimate-guide-0ea18a676311", "learn9_button"),  # Added link
      ],
   }

   for col, data in button_data.items():
      with col:
         for i, (label, image_path, link, key) in enumerate(data):
               centered_link_button(col, label, image_path, link, key)
         st.markdown("<h3 style='margin-bottom: -45px'><br></h3>", unsafe_allow_html=True)
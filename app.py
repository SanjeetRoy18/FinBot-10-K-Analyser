import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

df = pd.read_csv('10K_M_T_A.csv')
df = df.sort_values(['Company', 'Fiscal Year']) 

def simple_chatbot(user_query):
    # Normalize input to handle lowercase/extra spaces
    query = user_query.strip()

    if query in ["What is the total revenue?", "1.", "1"]:
        result = df.groupby('Company')['Total Revenue'].sum()
        return f"Total revenue (in millions) (2023-25): \n{result}"
        
    elif query in ["How has net income changed over the years?", "2.", "2"]:
        result = df[['Company', 'Fiscal Year', 'Net Income']].to_string(index=False)
        return f"Net Income Changes (in millions): \n{result}"
        
    elif query in ["What is the net profit margin?", "3.", "3"]:
        df['Net Profit Margin (%)'] = (df['Net Income'] / df['Total Revenue']) * 100
        result = df[['Company', 'Fiscal Year', 'Net Profit Margin (%)']].to_string(index=False)
        return f"Net Profit Margins (in millions): \n{result}"
        
    elif query in ["Which company has the highest revenue?", "4.", "4"]:
        best = df.groupby('Company')['Total Revenue'].sum().idxmax()
        return f"The company with the highest total revenue (in millions) (2023-2025) is: {best}"

    elif query in ["What is the revenue growth?", "5.", "5"]:
        df['Revenue Growth (%)'] = df.groupby('Company')['Total Revenue'].pct_change() * 100
        result = df[['Company', 'Fiscal Year', 'Revenue Growth (%)']].dropna().to_string(index=False)
        return f"Revenue Growth (%) (in millions):\n{result}"

    else:
        return "Sorry, I can only answer predefined queries. Try one of these:\n" \
                "1. What is the total revenue?\n" \
                "2. How has net income changed over the years?\n" \
                "3. What is the net profit margin?\n" \
                "4. Which company has the highest revenue?\n" \
                "5. What is the revenue growth?"
         

print(" Hi, Financial Chatbot here.")
print("Try asking one of these questions:\n" \
               "1. What is the total revenue?\n" \
               "2. How has net income changed over the years?\n" \
               "3. What is the net profit margin?\n" \
               "4. Which company has the highest revenue?\n" \
               "5. What is the revenue growth?")
print("(type 'exit' to quit)\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    print("Bot:", simple_chatbot(user_input))
    print()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    reply = simple_chatbot(user_msg)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=False, port=8080)
from flask import Flask,request,jsonify,render_template
from groq import Groq

app=Flask(__name__)

GROQ_API_KEY="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"
client=Groq(api_key=GROQ_API_KEY)

with open("knowledge.txt","r",encoding="utf-8")as file:
    knowledge=file.read()#file read content store in knowledge var.

#create server
@app.route("/")#/ means we are creating home page

def home():
    return render_template("index.html")

@app.route("/chat",methods=['POST'])#for backend
def chat():
    user_message=request.json.get("message")
    if user_message.lower() in ["hi","hello","hey","hii"]:
        return jsonify({"reply":"Hello👋😊! I am SQL Query Optimization Chatbot,How can i help you?"})
    if user_message.lower() in ["Thanks","Thank you","by","bye"]:
        return jsonify({"reply":"I'm here whenever you need me. bye👋😊,Take care!"})
    
    #Create one request to LLM
    completion=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
                {
                    "role": "system",
                    "content": f"""
                    You are a Frontend Performance Optimization Assistant. Help developers improve website speed, Core Web Vitals, and overall performance.

                    ### CONTEXT (KNOWLEDGE BASE SUMMARY):
                    {knowledge}

                    ### INSTRUCTIONS:
                    1. Use the knowledge listed above to provide accurate technical advice.
                    2. Give clear, actionable suggestions with simple explanations and code examples when needed.
                    3. Keep responses concise and structured.

                    If a question is outside these topics, reply:
                    Sorry, I don’t have knowledge about that. I can help with:
                    1. Website speed and loading performance
                    2. Core Web Vitals optimization
                    3. Efficient UI rendering performance
                    4. Reducing layout shifts and improving responsiveness
                    """
                },
                {
                    "role": "user", 
                    "content": user_message
                }
            ],
    )
    bot_reply=completion.choices[0].message.content
    return jsonify({"reply":bot_reply})

#All function call
if __name__=="__main__":app.run(debug=True)
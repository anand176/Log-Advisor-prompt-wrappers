from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set the Gemini API key
api_key = 'api_key'  # Ensure your API key is stored in an .env file
genai.configure(api_key=api_key)

def get_gemini_response(prompt):
    """Function to get a response from the Gemini API."""
    try:
        # Create a generative model instance
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        
        # Generate content based on the provided prompt
        response = model.generate_content([prompt], request_options={"timeout": 600})
        
        # Return the response text
        return response.text
        
    except Exception as e:
        return f"Error while communicating with Gemini API: {e}"

@app.route("/analyze_sequence", methods=["POST"])
def analyze_sequence():
    """API endpoint to receive a sequence and return an analysis."""
    data = request.json
    if 'sequence' not in data:
        return jsonify({"error": "No sequence provided"}), 400
    
    # The sequence of events is passed in the 'sequence' key
    sequence = data['sequence']
    
    # Create a prompt using the sequence
    prompt = (
        "can you identify what anomaly is happening from a group of events happening in hdfs. "
        "here are all the events in the hdfs EventId,EventTemplate "
        "E5,Receiving block <*> src: /<*> dest: /<*> E22,BLOCK* NameSystem.allocateBlock:<*> "
        "E11,PacketResponder <*> for block <*> terminating E9,Received block <*> of size <*> from /<*> "
        "E26,BLOCK* NameSystem.addStoredBlock: blockMap updated: <*> is added to <*> size <*> "
        "E6,Received block <*> src: /<*> dest: /<*> of size <*> "
        "E16,<*>:Transmitted block <*> to /<*> E18,<*> Starting thread to transfer block <*> to <*> "
        "E25,BLOCK* ask <*> to replicate <*> to datanode(s) <*> E3,<*> Served block <*> to /<*> "
        "E2,Verification succeeded for <*> E7,writeBlock <*> received exception <*> "
        "E10,PacketResponder <*> <*> Exception <*> E21,Deleting block <*> file <*> "
        "E13,Receiving empty packet for block <*> E14,Exception in receiveBlock for block <*> <*> "
        "E27,BLOCK* NameSystem.addStoredBlock: Redundant addStoredBlock request received for <*> on <*> size <*> "
        "E8,PacketResponder <*> for block <*> Interrupted. "
        "E15,Changing block file offset of block <*> from <*> to <*> meta file offset to <*>. "
        f"Here is the sequence: {sequence}."
    )

    # Get the response from Gemini API
    response = get_gemini_response(prompt)

    # Return the response as JSON
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

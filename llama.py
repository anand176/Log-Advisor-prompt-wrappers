# server.py
from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

# Route to handle sequence analysis
@app.route('/analyze', methods=['POST'])
def analyze_sequence():
    data = request.json
    sequence = data.get('sequence')

    # Define the HDFS events
    hdfs_events = """
    EventId,EventTemplate
    E5,Receiving block <*> src: /<*> dest: /<*>
    E22,BLOCK* NameSystem.allocateBlock:<*>
    E11,PacketResponder <*> for block <*> terminating
    E9,Received block <*> of size <*> from /<*>
    E26,BLOCK* NameSystem.addStoredBlock: blockMap updated: <*> is added to <*> size <*>
    E6,Received block <*> src: /<*> dest: /<*> of size <*>
    E16,<*>:Transmitted block <*> to /<*>
    E18,<*> Starting thread to transfer block <*> to <*>
    E25,BLOCK* ask <*> to replicate <*> to datanode(s) <*>
    E3,<*> Served block <*> to /<*>
    E2,Verification succeeded for <*>
    E7,writeBlock <*> received exception <*>
    E10,PacketResponder <*> <*> Exception <*>
    E21,Deleting block <*> file <*>
    E13,Receiving empty packet for block <*>
    E14,Exception in receiveBlock for block <*> <*>
    E27,BLOCK* NameSystem.addStoredBlock: Redundant addStoredBlock request received for <*> on <*> size <*>
    E8,PacketResponder <*> for block <*> Interrupted.
    E15,Changing block file offset of block <*> from <*> to <*> meta file offset to <*>.
    """

    # Create prompt for ollama
    prompt = (
        "Here are all the events in the HDFS (EventId, EventTemplate):\n"
        f"{hdfs_events}. I will now give you a sequence, can you identify what is happening "
        f"in the block {sequence} and give possible anomalies in the block in short."
    )

    # Call ollama API
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    # Return the ollama response
    return jsonify({'response': response["message"]["content"]})

if __name__ == '__main__':
    app.run(debug=True)

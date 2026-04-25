const uploadForm = document.getElementById('uploadForm');
const statusBox = document.getElementById('status');
const statusMsg = document.getElementById('statusMessage');

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];

    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    statusBox.className = "status-box";
    statusMsg.innerText = "Processing your firewall rules...";
    statusBox.classList.remove('hidden');

    try {
        /* 5. THE HANDSHAKE (Fetch API)
           We send the data to the backend. 
           NOTE: 'http://127.0.0.1:5000/upload' is a placeholder. 
           Your teammates will give you their actual server URL later.
        */
        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            statusBox.classList.add('success');
            statusMsg.innerText = "Rules analyzed successfully!";
            
            console.log("Data from Python:", data);
            console.log("Raw CSV Contents:", data.raw_data);
        } else {
            throw new Error("Backend server error");
        }
    } catch (error) {
        statusBox.classList.add('error');
        statusMsg.innerText = "Could not connect to the backend server.";
        console.error("Connection Error:", error);
    }
});
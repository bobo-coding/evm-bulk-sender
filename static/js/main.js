// Replace or update the CSV file handling code
document.getElementById('csvFile').addEventListener('change', async function(event) {
    const file = event.target.files[0];
    if (file) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            setStatus("Uploading CSV file...", "pending");
            
            const response = await fetch('/upload-csv', {
                method: 'POST',
                body: formData
                // Don't set Content-Type header - FormData sets it automatically with boundary
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Failed to upload CSV");
            }
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Clear existing rows
            const recipientsBody = document.getElementById('recipientsBody');
            recipientsBody.innerHTML = '';
            
            // Add new rows
            if (data.recipients && data.recipients.length > 0) {
                data.recipients.forEach(recipient => {
                    addRecipientRow(recipient.address, recipient.amount);
                });
                setStatus(`Successfully loaded ${data.recipients.length} recipients from CSV`, "success");
            } else {
                setStatus("No valid recipients found in CSV file", "warning");
            }
        } catch (error) {
            console.error("Error processing CSV:", error);
            setStatus("Error processing CSV: " + error.message, "error");
        }
    }
});

// Helper function for status messages if not already defined
function setStatus(message, type) {
    const statusEl = document.getElementById('transactionStatus');
    if (!statusEl) return;
    
    statusEl.textContent = message;
    statusEl.className = '';
    
    switch (type) {
        case 'pending':
            statusEl.classList.add('status-pending');
            break;
        case 'success':
            statusEl.classList.add('status-success');
            break;
        case 'error':
            statusEl.classList.add('status-error');
            break;
        case 'warning':
            statusEl.classList.add('status-warning');
            break;
    }
} 
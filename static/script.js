async function performScrapej() {
    const url = document.getElementById('websiteUrl').value;
    const query = document.getElementById('userQuery').value;
    
    if (!url || !query) {
        alert('Please fill in both fields');
        return;
    }
    
    // Show loading indicator
    document.getElementById('loadingIndicator').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');

    
    try {
        const response = await fetch('/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url, query })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Use marked.parse() to render markdown
            document.getElementById('resultContent').innerHTML = 
                marked.parse(data.result);
        } else {
            document.getElementById('resultContent').innerHTML = 
                `<div class="error">Error: ${data.error}</div>`;
        }
    } catch (error) {
        document.getElementById('resultContent').innerHTML = 
            `<div class="error">Error: ${error.message}</div>`;
    } finally {
        document.getElementById('loadingIndicator').classList.add('hidden');
        document.getElementById('results').classList.remove('hidden');
    }
}
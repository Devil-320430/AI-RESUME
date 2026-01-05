document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    
    submitBtn.disabled = true;
    loading.style.display = 'block';
    results.innerHTML = '';
    
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loading.style.display = 'none';
        submitBtn.disabled = false;
        
        if (data.error) {
            results.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            return;
        }
        
        results.innerHTML = `
            <h2>Analysis Results</h2>
            <div class="score-wrapper">
                <svg class="progress-ring" width="140" height="140">
                    <circle
                        class="progress-ring__background"
                        cx="70"
                        cy="70"
                        r="60"
                    />
                    <circle
                        class="progress-ring__circle"
                        cx="70"
                        cy="70"
                        r="60"
                        stroke-dasharray="377"
                        stroke-dashoffset="${377 - (377 * data.score) / 100}"
                    />
                </svg>
                <div class="score-text">${data.score}</div>
                <div class="score-label"><h3>Score</h3></div>
            </div>
            <h3>Matched Skills:</h3>
            <p>${data.matched.length > 0 ? data.matched.join(', ') : 'None'}</p>
            <h3>Missing Skills:</h3>
            <p>${data.missing.length > 0 ? data.missing.join(', ') : 'None'}</p>
            <h3>AI Suggestions:</h3>
            <p>${data.suggestions}</p>
        `;
    })
    .catch(error => {
        loading.style.display = 'none';
        submitBtn.disabled = false;
        results.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    });
});
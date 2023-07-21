function getVideoData(bvNumber) {
    const apiURL = '/get_subtitles';
    return fetch(apiURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ bv_number: bvNumber })
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error:', error);
        return null;
    });
}

function submitLink() {
    const linkInput = document.getElementById('linkInput').value;
    // Send the linkInput to the server (Flask backend)
    getVideoData(linkInput)
        .then(data => {
            if (data.valid) {
                const subtitles = data.subtitles;
                console.log(subtitles); // Replace with your desired handling of subtitles
            } else {
                console.log(data.error || 'Invalid link. Please enter a valid Bilibili video link.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

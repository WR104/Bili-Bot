function getVideoData(videoUrl) {
    const apiURL = '/get';
    return fetch(apiURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ video_url: videoUrl })
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
                const info = data.response;
                console.log(info); // Replace with your desired handling of subtitles
            } else {
                console.log(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

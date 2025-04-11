document.addEventListener('DOMContentLoaded', function() {
    const videoInput = document.getElementById('videoInput');
    const audioInput = document.getElementById('audioInput');
    const costumeInput = document.getElementById('costumeInput');
    const voiceSampleInput = document.getElementById('voiceSampleInput');
    const generateButton = document.getElementById('generateButton');
    const status = document.getElementById('status');
    const downloadLink = document.getElementById('downloadLink');
    const ttsText = document.getElementById('ttsText');

    // Function to validate file extensions
    function isValidFileType(file, allowedExtensions) {
        return allowedExtensions.some(ext => file.name.endsWith(ext));
    }

    // Function to update the status
    function updateStatus(message) {
        status.textContent = message;
    }

    // Function to show loading spinner
    function showLoading() {
      generateButton.disabled = true;
      generateButton.innerHTML = '<span class="spinner"></span> Processing...';
      downloadLink.style.display = 'none';
    }

    // Function to hide loading spinner
    function hideLoading() {
        generateButton.disabled = false;
        generateButton.textContent = 'Generate Video';
    }
    
    // Function to enable download link
    function enableDownload() {
        downloadLink.style.display = 'block';
    }

    // Event listeners for file inputs
    videoInput.addEventListener('change', function() {
        if (!isValidFileType(this.files[0], ['.mp4'])) {
            alert('Invalid video file type. Please upload an .mp4 file.');
            this.value = '';
        }
    });

    audioInput.addEventListener('change', function() {
        if (!isValidFileType(this.files[0], ['.wav'])) {
            alert('Invalid audio file type. Please upload a .wav file.');
            this.value = '';
        }
    });

    costumeInput.addEventListener('change', function() {
        if (!isValidFileType(this.files[0], ['.jpg', '.jpeg'])) {
            alert('Invalid costume file type. Please upload a .jpg or .jpeg file.');
            this.value = '';
        }
    });
    voiceSampleInput.addEventListener('change', function() {
        if (!isValidFileType(this.files[0], ['.wav'])) {
            alert('Invalid voice sample file type. Please upload a .wav file.');
            this.value = '';
        }
    });

    // Event listener for generate button
    generateButton.addEventListener('click', function() {
        if (!videoInput.files.length || !audioInput.files.length) {
          alert('Please upload both a video and an audio file.');
          return;
        }
        showLoading();
        updateStatus('Processing...');

        // Simulate processing time (replace with actual backend call)
        setTimeout(() => {
            // Mock API call - Replace with actual API call
            console.log('Mock API call to backend to process files and settings');

            // Backend integrations (replace with actual backend logic)
            // Use Whisper to transcribe audio if no TTS provided
            if (!ttsText.value) {
              console.log("// Use Whisper to transcribe audio");
            } else {
              console.log("// Use Coqui TTS to generate audio from TTS text");
            }
            console.log('// Use Mediapipe to track poses in the video.');
            console.log('// Use FFmpeg to handle video extension and reassembly.');
            console.log('// Use LatentSync for lip-syncing the video.');
            console.log('// Use MuseTalk for full-face animation on the video.');
            console.log('// Use Stable Diffusion Inpainting to perform costume swaps.');

            // Mock response from backend
            updateStatus('Done!');
            hideLoading();
            enableDownload();
        }, 2000); // Simulate 2 seconds processing
    });
});
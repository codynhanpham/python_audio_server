// GLOBAL VARIABLES
let AudioLists = {};
let PlaylistLists = {};
let LastSelection = {
    playlist: null,
    audio: null
};
let isPlaying = false; // To keep track of the current state of the audio playback
let playbackFetchController = null; playbackFetchSignal = null;
// check if AbortController is supported
if ('AbortController' in window) {
    playbackFetchController = new AbortController(); // To keep track of the current fetch request for audio playback, to handle /restart requests gracefully
    playbackFetchSignal = playbackFetchController.signal;
}



// Known elements, set to null if not found or not intialized yet
let gaplessCheckbox = document.getElementById('gapless-checkbox-group') || null;
let playbackTypeDropdown = document.getElementById('playback-type-dropdown') || null;
let playbackFileDropdown = document.getElementById('playback-file-dropdown') || null;
let generateToneSweepTypeDropdown = document.getElementById('generate-tonesweep-type-dropdown') || null;
let generateToneSweepStartFreq = document.getElementById('generate-tonesweep-freq') || null;
let generateToneSweepEndFreq = document.getElementById('generate-tonesweep-freq-end') || null;
let generateToneSweepDuration = document.getElementById('generate-tonesweep-duration') || null;
let generateToneSweepAmplitude = document.getElementById('generate-tonesweep-amplitude') || null;
let generateToneSweepSampleRate = document.getElementById('generate-tonesweep-samplerate') || null;
let generateToneSweepFn = document.getElementById('generate-tonesweep-sweepfn-dropdown') || null;
let generateToneSweepEdge = document.getElementById('generate-tonesweep-edge') || null;



// Custom Number Spinner Functions
function updateNumberSpinner(element) {
    // This is a up or down button, indicated by this.value

    let parentDiv = element.parentElement;

    // Get the min, max, step, and default values,... from the parent div
    let min = parseFloat(parentDiv.getAttribute('data-min'));
    let max = parseFloat(parentDiv.getAttribute('data-max'));
    let step = parseFloat(parentDiv.getAttribute('data-step')) || 1;
    let defaultValue = parseFloat(parentDiv.getAttribute('data-default')) || min || 0;
    let isInt = parentDiv.getAttribute('data-integer') === 'true' ? true : false;
    let scaler = parentDiv.getAttribute('data-scale') || "linear"; // linear or log2 or logarithmic

    let currentValue = parseFloat(parentDiv.querySelector('input').value) || defaultValue;

    // Get the current value from the input element
    let changeDirection = element.value === 'up' ? 1 : -1;
    // newValue depends on the currentValue, step, and scaler: if linear, then it's the step, if log2, then either double or half, if logarithmic, then either 10x or 0.1x
    let newValue = currentValue;
    if (scaler === "linear") {
        newValue += step * changeDirection;
    } else if (scaler === "log2") {
        newValue *= Math.pow(2, changeDirection);
    } else if (scaler === "logarithmic") {
        newValue *= Math.pow(10, changeDirection);
    }

    // if isInt is true, then round it to the nearest integer
    if (isInt) {
        newValue = Math.round(newValue);
    }

    // Check if the new value is within the min and max range
    if (newValue < min) {
        newValue = min;
    } else if (newValue > max) {
        newValue = max;
    }

    // Always limit to 5 decimal places if value is a float
    if (!Number.isInteger(newValue)) {
        newValue = parseFloat(newValue.toFixed(5));
    }

    // Update the input element with the new value
    parentDiv.querySelector('input').value = newValue;
    // Update step for the parentDiv as well for the next time
    parentDiv.setAttribute('data-step', step);
    // Trigger the input event to format the value and update the tooltip title
    parentDiv.querySelector('input').dispatchEvent(new Event('input'));
}
function validateNumberSpinner(element) {
    // Fires when the input element value changes
    // This is the input element: validate the value and update the input element with the new value

    let parentDiv = element.parentElement;

    // Get the min, max, step, and default values,... from the parent div
    let min = parseFloat(parentDiv.getAttribute('data-min'));
    let max = parseFloat(parentDiv.getAttribute('data-max'));
    let step = parseFloat(parentDiv.getAttribute('data-step')) || 1;
    let defaultValue = parseFloat(parentDiv.getAttribute('data-default')) || min || 0;
    let isInt = parentDiv.getAttribute('data-integer') === 'true' ? true : false;
    
    // Set the attributes of the input element only if they are numbers and not Inf
    if (!isNaN(min) && min != this.min) {
        element.setAttribute('min', min);
    }
    if (!isNaN(max) && max != this.max) {
        element.setAttribute('max', max);
    }
    if (!isNaN(step) && step != this.step) {
        element.setAttribute('step', step);
    }

    // Get the current value from the input element
    let currentValue = parseFloat(element.value) || defaultValue;

    // if the currentValue is not int and isInt is true, then round it to the nearest integer
    if (!Number.isInteger(currentValue) && isInt) {
        currentValue = Math.round(currentValue);
    }

    // Check if the new value is within the min and max range
    if (currentValue < min) {
        currentValue = min || defaultValue;
    } else if (currentValue > max) {
        currentValue = max || defaultValue;
    }

    // Always limit to 5 decimal places if currentValue is a float
    if (!Number.isInteger(currentValue)) {
        currentValue = parseFloat(currentValue.toFixed(5));
    }

    // Update the input element with the new value, overwrite the value if it's different
    if (element.value !== currentValue) {
        element.value = currentValue;
    }

    // Lastly, update tooltip title with min, max, and type of number
    if (min === null || isNaN(min) || min === undefined) {
        min = "-∞"
    } else {
        min = min.toLocaleString();
    }
    if (max === null || isNaN(max) || max === undefined) {
        max = "+∞"
    } else {
        max = max.toLocaleString();
    }
    let tooltipTitle = `Enter ${isInt ? 'an integer' : 'a number'} between ${min} and ${max} (inclusive)`;

    if (element.title !== tooltipTitle) {
        element.title = tooltipTitle;
    }
}
function updateAllSpinnersInputAttributes() {
    // Select class .number-spinner, then its div > input element and update the input attributes
    document.querySelectorAll('.number-spinner').forEach(function(element) {
        let inputElement = element.querySelector('input');
        validateNumberSpinner(inputElement);
    });
}


// GENERAL TABS FUNCTIONS

function openTab(evt, tabName) {
    let i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function pointerScroll(elem) {
    let isDrag = false;
    
    const dragStart = () => isDrag = true;
    const dragEnd = () => isDrag = false;
    const drag = (ev) => isDrag && (elem.scrollLeft -= ev.movementX);
    
    elem.addEventListener("pointerdown", dragStart);
    addEventListener("pointerup", dragEnd);
    addEventListener("pointermove", drag);
};



// ------- PLAY FILES TAB FUNCTIONS ------- //

function refreshAudioPlaylistLists() {
    // Fetch /list?json=true to get the list of all available media
    fetch('/list?json=true')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            AudioLists = data.audio || {};
            PlaylistLists = data.playlist || {};

            // Populate the audio list onto the #playback-file select element
            // clear the current options as they might be outdated
            playbackFileDropdown.innerHTML = '';
            updatePlaybackType(playbackTypeDropdown.value); // use the current selected playback Type (audio or playlist) to update the dropdown
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
        });
}


function updatePlaybackType(value) {
    // Replace the content of the #playback-file-dropdown select element with the appropriate list
    playbackFileDropdown.innerHTML = '';
    if (value === 'play') {
        for (let key in AudioLists) {
            let option = document.createElement('option');
            option.value = AudioLists[key];
            option.text = AudioLists[key];
            playbackFileDropdown.appendChild(option);
        }

        // Toggle the gapless checkbox visibility
        gaplessCheckbox.classList.add('visible-toggle');
    } else if (value === 'playlist') {
        for (let key in PlaylistLists) {
            let option = document.createElement('option');
            option.value = PlaylistLists[key];
            option.text = PlaylistLists[key];
            playbackFileDropdown.appendChild(option);
        }

        // Toggle the gapless checkbox visibility
        gaplessCheckbox.classList.remove('visible-toggle');
    }

    // Set the dropdown to the last selected value or the first value if it's the first time
    if (value === 'play') {
        if (LastSelection.audio && AudioLists.includes(LastSelection.audio)) {
            playbackFileDropdown.value = LastSelection.audio;
        } else {
            playbackFileDropdown.value = AudioLists[0];
        }
    } else if (value === 'playlist') {
        if (LastSelection.playlist && PlaylistLists.includes(LastSelection.playlist)) {
            playbackFileDropdown.value = LastSelection.playlist;
        } else {
            playbackFileDropdown.value = PlaylistLists[0];
        }
    }

    // Update the last selected value
    if (value === 'play') {
        LastSelection.audio = playbackFileDropdown.value;
    } else if (value === 'playlist') {
        LastSelection.playlist = playbackFileDropdown.value;
    }


    // Update the #file-info-data in the [Info] tab
    const fileInfoDataElement = document.getElementById('file-info-data');
    // Fetch /info/<value> to get the file info. The server response as plain text
    const currentFile = playbackFileDropdown.value;
    fetch(`/info/${currentFile}`)
        .then(response => response.text())
        .then(data => {
            fileInfoDataElement.innerText = data;
        
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
        });
}

function updatePlaybackFile(value) {
    // Update the last selected value
    let playbackType = playbackTypeDropdown.value;
    // play --> audio
    // playlist --> playlist
    if (playbackType === 'play') {
        LastSelection.audio = value;
    } else if (playbackType === 'playlist') {
        LastSelection.playlist = value;
    }


    // Update the #file-info-data in the [Info] tab
    const fileInfoDataElement = document.getElementById('file-info-data');
    // Fetch /info/<value> to get the file info. The server response as plain text
    fetch(`/info/${value}`)
        .then(response => response.text())
        .then(data => {
            fileInfoDataElement.innerText = data;
        
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
        });
}

function playRequest() {
    let playbackType = playbackTypeDropdown.value;
    let playbackFile = playbackFileDropdown.value;
    let withGapless = document.getElementById('gapless-checkbox').checked;

    if (!playbackType || !playbackFile) {
        return;
    }

    // Add a red border to the tabcontent-wrapper to indicate that the request is being processed
    document.getElementById('tabcontent-wrapper').classList.add('red-border-highlight');
    // Replace the #playback-play-button with the #playback-stop-button
    document.getElementById('playback-play-button').style.display = 'none';
    document.getElementById('playback-stop-button').style.display = 'block';

        
    // GET /<type>/<file>?time=<time in nanosec>
    // if type is playlist, then also check for gapless: /playlist/<file>?time=<time in nanosec> or /playlist/gapless/<file>?time=<time in nanosec>
    let url = `/${playbackType}/${playbackFile}?time=${Date.now() * 1000000}`;
    if (playbackType === 'playlist' && withGapless) {
        url = `/playlist/gapless/${playbackFile}?time=${Date.now() * 1000000}`;
    }
    
    isPlaying = true;
    fetch(url, { signal: playbackFetchSignal })
        .then(response => response.json())
        .then(data => {
            isPlaying = false;
            console.log(data);
            // Remove the red border from the tabcontent-wrapper to indicate that the request is done
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // Replace the #playback-stop-button with the #playback-play-button
            document.getElementById('playback-stop-button').style.display = 'none';
            document.getElementById('playback-play-button').style.display = 'block';
        })
        .catch(error => {
            isPlaying = false;
            // if abort, then the request was aborted by the user, so do not alert
            if (error.name === 'AbortError') {
                console.log('Request aborted. Most likely, the server has been restarted.');
                // reset the controller and signal
                playbackFetchController = new AbortController();
                playbackFetchSignal = playbackFetchController.signal;
            }
            else {
                console.error('Error:', error);
                alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
            }
            // Remove the red border from the tabcontent-wrapper to indicate that the request is done
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // Replace the #playback-stop-button with the #playback-play-button
            document.getElementById('playback-stop-button').style.display = 'none';
            document.getElementById('playback-play-button').style.display = 'block';
        });
}

function playbackStopAudio() {
    // Add a red border to the tabcontent-wrapper to indicate that the request is being processed
    document.getElementById('tabcontent-wrapper').classList.add('red-border-highlight');
    fetch('/stop')
        .then(response => response.json())
        .then(data => {
            isPlaying = false;
            console.log(data);
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // Replace the #playback-stop-button with the #playback-play-button
            document.getElementById('playback-stop-button').style.display = 'none';
            document.getElementById('playback-play-button').style.display = 'block';
        })
        .catch(error => {
            // Unsure if still playing or not, do not set isPlaying to false, and the if the audio is still playing, playRequest() will take care of it when the audio stops
            // _

            console.error('Error:', error);
            alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');

            if (!isPlaying) { // Best guestimate if the audio is still playing then keep the red border and the stop button
                document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
                // Replace the #playback-stop-button with the #playback-play-button
                document.getElementById('playback-stop-button').style.display = 'none';
                document.getElementById('playback-play-button').style.display = 'block';
            }
        });
}



// ------- GENERATE TAB FUNCTIONS ------- //

function updateToneSweepType(value) {
    // Hide/show the appropriate input fields based on the selected type
    // If tone, there is no end frequency or sweep function
    // If sweep, enable these again (with disabled-toggle class)
    const endfreqWrapper = document.getElementById('generate-tonesweep-freq-end-wrapper');
    const endfreqSpinner = document.getElementById('generate-tonesweep-freq-end-spinner');
    const fnWrapper = document.getElementById('generate-tonesweep-sweepfn-dropdown-wrapper');
    const playButton = document.getElementById('generate-tonesweep-play-button'); // innerText "▶ Play Tone" or "▶ Play Sweep"

    if (value === 'tone') {
        generateToneSweepEndFreq.disabled = true;
        generateToneSweepFn.disabled = true;
        // Add the disabled-toggle class to the wrapper to blur + disable it
        endfreqWrapper.classList.add('disabled-toggle');
        fnWrapper.classList.add('disabled-toggle');
        // Also disable the buttons inside of the spinner
        endfreqSpinner.querySelectorAll('button').forEach(button => button.disabled = true);
        playButton.innerText = "▶ Play Tone";

    } else if (value === 'sweep') {
        generateToneSweepEndFreq.disabled = false;
        generateToneSweepFn.disabled = false;
        // Remove the disabled-toggle class to the wrapper
        endfreqWrapper.classList.remove('disabled-toggle');
        fnWrapper.classList.remove('disabled-toggle');
        // Also enable the buttons inside of the spinner
        endfreqSpinner.querySelectorAll('button').forEach(button => button.disabled = false);
        playButton.innerText = "▶ Play Sweep";
    }
}


function updateNumberSpinnerEdge(element) {
    // A special case for the edge spinner, as it depends on the type of tone sweep and the duration spinner

    const generateToneSweepType = generateToneSweepTypeDropdown.value;
    let duration = parseFloat(generateToneSweepDuration.value);

    // If type is Tone, edge can be any positive value, and if it's negative, the absolute value must <= Duration /2
    // If type is Sweep, edge must be negative, and the absolute value must <= Duration /2

    // This is a up or down button, indicated by this.value

    let parentDiv = element.parentElement;

    // Get the min, max, step, and default values,... from the parent div
    let min = NaN; // comparison with NaN is always false
    let max = NaN; // comparison with NaN is always false
    let step = parseFloat(parentDiv.getAttribute('data-step')) || 1;
    let defaultValue = parseFloat(parentDiv.getAttribute('data-default')) || min || 0;
    let isInt = parentDiv.getAttribute('data-integer') === 'true' ? true : false;
    let scaler = parentDiv.getAttribute('data-scale') || "linear"; // linear or log2 or logarithmic

    let currentValue = parseFloat(parentDiv.querySelector('input').value) || defaultValue;


    // Change min and max based on the type of tone sweep and the duration
    console.log(generateToneSweepType, duration)
    if (generateToneSweepType === 'tone') {
        min = -duration / 2;
    }
    else if (generateToneSweepType === 'sweep') {
        max = 0;
        min = -duration / 2;
    }

    // Get the current value from the input element
    let changeDirection = element.value === 'up' ? 1 : -1;
    // newValue depends on the currentValue, step, and scaler: if linear, then it's the step, if log2, then either double or half, if logarithmic, then either 10x or 0.1x
    let newValue = currentValue;
    if (scaler === "linear") {
        newValue += step * changeDirection;
    } else if (scaler === "log2") {
        newValue *= Math.pow(2, changeDirection);
    } else if (scaler === "logarithmic") {
        newValue *= Math.pow(10, changeDirection);
    }

    // if isInt is true, then round it to the nearest integer
    if (isInt) {
        newValue = Math.round(newValue);
    }

    // Check if the new value is within the min and max range
    console.log(newValue, min, max)
    if (newValue < min) {
        newValue = min;
    } else if (newValue > max) {
        newValue = max;
    }

    // Always limit to 5 decimal places if value is a float
    if (!Number.isInteger(newValue)) {
        newValue = parseFloat(newValue.toFixed(5));
    }

    // Update the input element with the new value
    parentDiv.querySelector('input').value = newValue;
    // Update step for the parentDiv as well for the next time
    parentDiv.setAttribute('data-step', step);
    // Trigger the input event to format the value and update the tooltip title
    parentDiv.querySelector('input').dispatchEvent(new Event('input'));
}
function validateNumberSpinnerEdge(element) {
    const generateToneSweepType = generateToneSweepTypeDropdown.value;
    let duration = parseFloat(generateToneSweepDuration.value);

    let parentDiv = element.parentElement;

    // Get the min, max, step, and default values,... from the parent div
    let min = NaN; // comparison with NaN is always false
    let max = NaN; // comparison with NaN is always false
    let step = parseFloat(parentDiv.getAttribute('data-step')) || 1;
    let defaultValue = parseFloat(parentDiv.getAttribute('data-default')) || min || 0;
    let isInt = parentDiv.getAttribute('data-integer') === 'true' ? true : false;
    
    // Set the attributes of the input element only if they are numbers and not Inf
    if (!isNaN(min) && min != this.min) {
        element.setAttribute('min', min);
    }
    if (!isNaN(max) && max != this.max) {
        element.setAttribute('max', max);
    }
    if (!isNaN(step) && step != this.step) {
        element.setAttribute('step', step);
    }

    // Get the current value from the input element
    let currentValue = parseFloat(element.value) || defaultValue;

    // if the currentValue is not int and isInt is true, then round it to the nearest integer
    if (!Number.isInteger(currentValue) && isInt) {
        currentValue = Math.round(currentValue);
    }

    // Change min and max based on the type of tone sweep and the duration
    if (generateToneSweepType === 'tone') {
        min = -duration / 2;
    }
    else if (generateToneSweepType === 'sweep') {
        max = 0;
        min = -duration / 2;
    }


    // Check if the new value is within the min and max range
    if (currentValue < min) {
        currentValue = min || defaultValue;
    } else if (currentValue > max) {
        currentValue = max || defaultValue;
    }

    // Always limit to 5 decimal places if currentValue is a float
    if (!Number.isInteger(currentValue)) {
        currentValue = parseFloat(currentValue.toFixed(5));
    }

    // Update the input element with the new value, overwrite the value if it's different
    if (element.value !== currentValue) {
        element.value = currentValue;
    }

    // Lastly, update tooltip title
    let tooltipTitle = "";
    if (generateToneSweepType === 'tone') {
        tooltipTitle = `Enter an integer, positive or negative. If negative, the absolute value must be less than or equal to half of the Duration.`;
    } else if (generateToneSweepType === 'sweep') {
        tooltipTitle = `Enter a negative integer. The absolute value must be less than or equal to half of the Duration.`;
    }
    if (element.title !== tooltipTitle) {
        element.title = tooltipTitle;
    }
}


function generatePlayToneSweep() {
    const generateToneSweepType = generateToneSweepTypeDropdown.value;
    const startFreq = parseFloat(generateToneSweepStartFreq.value);
    const endFreq = parseFloat(generateToneSweepEndFreq.value);
    const duration = parseFloat(generateToneSweepDuration.value);
    const amplitude = parseFloat(generateToneSweepAmplitude.value);
    const sampleRate = parseFloat(generateToneSweepSampleRate.value);
    const fn = generateToneSweepFn.value;
    const edge = parseFloat(generateToneSweepEdge.value);

    // if any of the values are NaN, then return
    if (isNaN(startFreq) || isNaN(duration) || isNaN(amplitude) || isNaN(sampleRate) || isNaN(edge)) {
        return;
    }

    // Add a red border to the tabcontent-wrapper to indicate that the request is being processed
    document.getElementById('tabcontent-wrapper').classList.add('red-border-highlight');
    // Replace the #playback-play-button with the #playback-stop-button
    document.getElementById('generate-tonesweep-play-button').style.display = 'none';
    document.getElementById('generate-tonesweep-stop-button').style.display = 'block';


    // Depends on the type of tone sweep, the URL will be different (see /docs for more info)

    let url = '';
    if (generateToneSweepType === 'tone') {
        url = `/tone/${startFreq}/${duration}/${amplitude}/${sampleRate}?edge=${edge}`;
    } else if (generateToneSweepType === 'sweep') {
        url = `/sweep/${fn}/${startFreq}/${endFreq}/${duration}/${amplitude}/${sampleRate}?edge=${edge}`;
    }
    if (!url) {
        return;
    }

    isPlaying = true;
    fetch(url, { signal: playbackFetchSignal })
        .then(response => response.json())
        .then(data => {
            isPlaying = false;
            console.log(data);
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // Replace the #generate-tonesweep-stop-button with the #generate-tonesweep-play-button
            document.getElementById('generate-tonesweep-stop-button').style.display = 'none';
            document.getElementById('generate-tonesweep-play-button').style.display = 'block';
        })
        .catch(error => {
            isPlaying = false;
            // if abort, then the request was aborted by the user, so do not alert
            if (error.name === 'AbortError') {
                console.log('Request aborted. Most likely, the server has been restarted.');
                // reset the controller and signal
                playbackFetchController = new AbortController();
                playbackFetchSignal = playbackFetchController.signal;
            }
            else {
                console.error('Error:', error);
                alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
            }
            // Remove the red border from the tabcontent-wrapper to indicate that the request is done
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // Replace the #generate-tonesweep-stop-button with the #generate-tonesweep-play-button
            document.getElementById('generate-tonesweep-stop-button').style.display = 'none';
            document.getElementById('generate-tonesweep-play-button').style.display = 'block';
        });
}

function generateStopAudio() {
    // Add a red border to the tabcontent-wrapper to indicate that the request is being processed
    document.getElementById('tabcontent-wrapper').classList.add('red-border-highlight');
    fetch('/stop')
        .then(response => response.json())
        .then(data => {
            isPlaying = false;
            console.log(data);
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // Replace the #generate-tonesweep-stop-button with the #generate-tonesweep-play-button
            document.getElementById('generate-tonesweep-stop-button').style.display = 'none';
            document.getElementById('generate-tonesweep-play-button').style.display = 'block';
        })
        .catch(error => {
            // Unsure if still playing or not, do not set isPlaying to false, and the if the audio is still playing, playRequest() will take care of it when the audio stops
            // _

            console.error('Error:', error);
            alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');

            if (!isPlaying) { // Best guestimate if the audio is still playing then keep the red border and the stop button
                document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
                // Replace the #generate-tonesweep-stop-button with the #generate-tonesweep-play-button
                document.getElementById('generate-tonesweep-stop-button').style.display = 'none';
                document.getElementById('generate-tonesweep-play-button').style.display = 'block';
            }
        });
}


function downloadToneSweep() {
    // Similar to play tone/sweep, but the route is /save_tone or /save_sweep
    const generateToneSweepType = generateToneSweepTypeDropdown.value;
    const startFreq = parseFloat(generateToneSweepStartFreq.value);
    const endFreq = parseFloat(generateToneSweepEndFreq.value);
    const duration = parseFloat(generateToneSweepDuration.value);
    const amplitude = parseFloat(generateToneSweepAmplitude.value);
    const sampleRate = parseFloat(generateToneSweepSampleRate.value);
    const fn = generateToneSweepFn.value;
    const edge = parseFloat(generateToneSweepEdge.value);

    // if any of the values are NaN, then return
    if (isNaN(startFreq) || isNaN(duration) || isNaN(amplitude) || isNaN(sampleRate) || isNaN(edge)) {
        return;
    }

    // Add a red border to the tabcontent-wrapper to indicate that the request is being processed
    document.getElementById('tabcontent-wrapper').classList.add('red-border-highlight');
    // Replace the add the disabled-toggle class to the #generate-tonesweep-download-button and disable it
    document.getElementById('generate-tonesweep-download-button').classList.add('disabled-toggle');
    document.getElementById('generate-tonesweep-download-button').disabled = true;


    // Depends on the type of tone sweep, the URL will be different (see /docs for more info)

    let url = '';
    if (generateToneSweepType === 'tone') {
        url = `/save_tone/${startFreq}/${duration}/${amplitude}/${sampleRate}?edge=${edge}`;
    } else if (generateToneSweepType === 'sweep') {
        url = `/save_sweep/${fn}/${startFreq}/${endFreq}/${duration}/${amplitude}/${sampleRate}?edge=${edge}`;
    }
    if (!url) {
        return;
    }

    // The server will respond with a file download
    fetch(url, { signal: playbackFetchSignal })
        .then(function(resp) {
            const header = resp.headers.get('Content-Disposition');
            if (!header) {
                filename = null;
                return resp.blob();
            }
            const parts = header.split(';');
            filename = parts[1].split('=')[1];
            return resp.blob();
        })
        .then(function(blob) {
            filename = filename.replace(/"/g, '');
            // download the blob as a file with the filename
            download(blob, filename, 'audio/wav');
            
            // Remove the red border from the tabcontent-wrapper to indicate that the request is done
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // Re enable the download button
            document.getElementById('generate-tonesweep-download-button').classList.remove('disabled-toggle');
            document.getElementById('generate-tonesweep-download-button').disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
            // Remove the red border from the tabcontent-wrapper to indicate that the request is done
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // Re enable the download button
            document.getElementById('generate-tonesweep-download-button').classList.remove('disabled-toggle');
            document.getElementById('generate-tonesweep-download-button').disabled = false;
        });
}





// ------- SETTINGS TAB FUNCTIONS ------- //

function reloadServerFiles() {
    // Fetch /reload to reload the server files. This will also stop the audio playback server-side if successful

    // Add a yellow border to the tabcontent-wrapper to indicate that the request is being processed
    document.getElementById('tabcontent-wrapper').classList.add('yellow-border-highlight');
    // temporarily disable the button #settings-reload-files: remove the ability to spam the reload button
    document.getElementById('settings-reload-files').style.pointerEvents = 'none';
    document.getElementById('settings-reload-files').style.opacity = '0.8';
    document.getElementById('settings-reload-files').classList.add('red-border-highlight')

    fetch('/reload')
        .then(_ => {
            isPlaying = false;
            console.log(_);
            refreshAudioPlaylistLists();
            // Remove the yellow border from the tabcontent-wrapper to indicate that the request is done
            document.getElementById('tabcontent-wrapper').classList.remove('yellow-border-highlight');
            // re-enable the button #settings-reload-files
            document.getElementById('settings-reload-files').style.pointerEvents = 'auto';
            document.getElementById('settings-reload-files').style.opacity = '1';
            document.getElementById('settings-reload-files').classList.remove('red-border-highlight')
        })
        .catch(error => {
            // Unsure if still playing or not, do not set isPlaying to false, and the if the audio is still playing, playRequest() will take care of it when the audio stops
            // _

            console.error('Error:', error);
            alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
            // Remove the yellow border from the tabcontent-wrapper to indicate that the request is done
            document.getElementById('tabcontent-wrapper').classList.remove('yellow-border-highlight');
            // re-enable the button #settings-reload-files
            document.getElementById('settings-reload-files').style.pointerEvents = 'auto';
            document.getElementById('settings-reload-files').style.opacity = '1';
            document.getElementById('settings-reload-files').classList.remove('red-border-highlight')

            // Since the server failed to reload, audio might still be playing, so at least keep the red border
            if (isPlaying) {
                document.getElementById('tabcontent-wrapper').classList.add('red-border-highlight');
            }
        });
}

function restartAudioServer() {
    // Fetch /restart?restart=true to restart the server
    // But first, confirm with the user if they really want to restart the server
    if (!confirm('Are you sure you want to restart the server?\n\nThis will shut down the server, stop all audio playback, and start the server again. This will take a few seconds to complete.')) {
        return;
    }

    // Add a red border to the tabcontent-wrapper to indicate that the request is being processed
    document.getElementById('tabcontent-wrapper').classList.add('red-border-highlight');
    // temporarily disable the button #settings-restart-server: remove the ability to spam the restart button
    document.getElementById('settings-restart-server').style.pointerEvents = 'none';
    document.getElementById('settings-restart-server').style.opacity = '0.8';
    document.getElementById('settings-restart-server').classList.add('red-border-highlight')

    if (isPlaying && ('AbortController' in window)) {
        playbackFetchController.abort(); // Abort the current fetch request for audio playback
    }
    fetch('/restart?restart=true')
        .then(response => response.json())
        .then(data => {
            isPlaying = false; // restart will also stop the audio playback if successful
            console.log(data);
            // Remove the red border from the tabcontent-wrapper to indicate that the request is done
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // re-enable the button #settings-restart-server
            document.getElementById('settings-restart-server').style.pointerEvents = 'auto';
            document.getElementById('settings-restart-server').style.opacity = '1';
            document.getElementById('settings-restart-server').classList.remove('red-border-highlight')

            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
            // Remove the red border from the tabcontent-wrapper to indicate that the request is done
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // re-enable the button #settings-restart-server
            document.getElementById('settings-restart-server').style.pointerEvents = 'auto';
            document.getElementById('settings-restart-server').style.opacity = '1';
            document.getElementById('settings-restart-server').classList.remove('red-border-highlight')

            // If this occur, it is not sure what the state of the server is, so alert to refresh the page
            alert('Click OK to try refreshing the page. If the server is still running, the page will refresh and you can continue using the server. Otherwise, you will need to manually refresh the page to continue using the server.');
            location.reload();
        });
}

function shutdownAudioServer() {
    // Fetch /shutdown?shutdown=YES_iamsureshutmedown to shutdown the server
    // But first, confirm with the user if they really want to shutdown the server
    if (!confirm('YOU WILL LOSE ACCESS TO THE SERVER CLIENT-SIDE!!\n\nAre you sure you want to shutdown the Audio Server?\nThis will completely shut down the server app. You will need to manually restart the server program to use it again. Only shutdown the server if you are sure you will not use it again in this session.')) {
        return;
    }

    // Add a red border to the tabcontent-wrapper to indicate that the request is being processed
    document.getElementById('tabcontent-wrapper').classList.add('red-border-highlight');
    // temporarily disable the button #settings-shutdown-server: remove the ability to spam the shutdown button
    document.getElementById('settings-shutdown-server').style.pointerEvents = 'none';
    document.getElementById('settings-shutdown-server').style.opacity = '0.8';
    document.getElementById('settings-shutdown-server').classList.add('red-border-highlight')

    fetch('/shutdown?shutdown=YES_iamsureshutmedown')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            token = data.shutdown_token;
            // For shutdown, the server will response with a token to really make sure the user wants to shutdown the server
            // Ask the user to confirm again
            if (!confirm('LAST CHANCE!!!\n\nAre you really sure you want to SHUTDOWN the Audio Server? After confirming, there is no going back. You will need to manually restart the server program to use it again.\n\n(If not confirm, this request will expire in 60 seconds)')) {
                if (!isPlaying) {
                    // Remove the red border from the tabcontent-wrapper to indicate that the request is done
                    document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
                }
                // re-enable the button #settings-shutdown-server
                document.getElementById('settings-shutdown-server').style.pointerEvents = 'auto';
                document.getElementById('settings-shutdown-server').style.opacity = '1';
                document.getElementById('settings-shutdown-server').classList.remove('red-border-highlight')
                return;
            }

            if ('AbortController' in window) {
                playbackFetchController.abort(); // Abort the current fetch request for audio playback
            }
            fetch(`/shutdown?token=${token}`) // Send the token to the server to confirm the shutdown
                .then(response => {
                    // If status is 400, the token was expired, so alert the user
                    if (response.status === 400) {
                        alert('Token expired after 60 seconds. If you have made up your mind to shutdown the server, try again.');
                    }
                    return response.json();
                })
                .then(data => {
                    isPlaying = false; // shutdown will also stop the audio playback if successful
                    console.log(data);
                    // Remove the red border from the tabcontent-wrapper to indicate that the request is done
                    document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
                    // re-enable the button #settings-shutdown-server
                    document.getElementById('settings-shutdown-server').style.pointerEvents = 'auto';
                    document.getElementById('settings-shutdown-server').style.opacity = '1';
                    document.getElementById('settings-shutdown-server').classList.remove('red-border-highlight')

                    alert("Server has been shutdown. You will need to manually restart the server program to use it again.");

                    // ask whether to refresh the page
                    if (confirm('Do you want to refresh the page to make sure?')) {
                        location.reload();
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
                    // Remove the red border from the tabcontent-wrapper to indicate that the request is done
                    document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
                    // re-enable the button #settings-shutdown-server
                    document.getElementById('settings-shutdown-server').style.pointerEvents = 'auto';
                    document.getElementById('settings-shutdown-server').style.opacity = '1';
                    document.getElementById('settings-shutdown-server').classList.remove('red-border-highlight')
                    // If this occur, it is not sure what the state of the server is, so alert to refresh the page
                    alert('Click OK to try refreshing the page. If the server is still running, the page will refresh and you can continue using the server. Otherwise, you will need to manually refresh the page to continue using the server.');
                    location.reload();
                });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
            // Remove the red border from the tabcontent-wrapper to indicate that the request is done
            document.getElementById('tabcontent-wrapper').classList.remove('red-border-highlight');
            // re-enable the button #settings-shutdown-server
            document.getElementById('settings-shutdown-server').style.pointerEvents = 'auto';
            document.getElementById('settings-shutdown-server').style.opacity = '1';
            document.getElementById('settings-shutdown-server').classList.remove('red-border-highlight')
            // If this occur, it is not sure what the state of the server is, so alert to refresh the page
            alert('Click OK to try refreshing the page. If the server is still running, the page will refresh and you can continue using the server. Otherwise, you will need to manually refresh the page to continue using the server.');
            location.reload();
        });
}





// ------- KEYBOARD SHORTCUTS ------- //

// Listen for "/" key to toggle #title-info display
window.addEventListener('keydown', function(e) {
    if (e.key === '/') {
        e.preventDefault();
        document.getElementById('title-info').classList.toggle('visible-toggle');
    }
}, false);



// ------- MAIN FUNCTION ON START UP ------- //

window.onload = function() {
    // Update known elements since the page has loaded
    gaplessCheckbox = document.getElementById('gapless-checkbox-group');
    playbackTypeDropdown = document.getElementById('playback-type-dropdown');
    playbackFileDropdown = document.getElementById('playback-file-dropdown');
    generateToneSweepTypeDropdown = document.getElementById('generate-tonesweep-type-dropdown');
    generateToneSweepStartFreq = document.getElementById('generate-tonesweep-freq');
    generateToneSweepEndFreq = document.getElementById('generate-tonesweep-freq-end');
    generateToneSweepDuration = document.getElementById('generate-tonesweep-duration');
    generateToneSweepAmplitude = document.getElementById('generate-tonesweep-amplitude');
    generateToneSweepSampleRate = document.getElementById('generate-tonesweep-samplerate');
    generateToneSweepFn = document.getElementById('generate-tonesweep-sweepfn-dropdown');
    generateToneSweepEdge = document.getElementById('generate-tonesweep-edge');


    // Fetch /list?json=true to get the list of all available media
    fetch('/list?json=true')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            AudioLists = data.audio || {};
            PlaylistLists = data.playlist || {};

            // Populate the audio list onto the #playback-file select element
            for (let key in AudioLists) {
                let option = document.createElement('option');
                option.value = AudioLists[key];
                option.text = AudioLists[key];
                playbackFileDropdown.appendChild(option);
            }

            // If no audio files are available, show a message in the dropdown
            if (Object.keys(AudioLists).length === 0) {
                let option = document.createElement('option');
                option.value = '';
                option.hidden = true;
                option.selected = true;
                option.text = 'Audio file or Playlist names will show up here!';
                playbackFileDropdown.appendChild(option);
            }

            // Update the #file-info-data in the [Info] tab
            const fileInfoDataElement = document.getElementById('file-info-data');
            // Fetch /info/<value> to get the file info. The server response as plain text
            const currentFile = playbackFileDropdown.value;
            if (currentFile) {
                fetch(`/info/${currentFile}`)
                    .then(response => response.text())
                    .then(data => {
                        fileInfoDataElement.innerText = data;
                    
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
                    });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error + '\n\nYou may want to check the console for more details (Ctrl + Shift + I).');
        });


    // When the page loads, open the default (Playback) tab
    document.getElementById("defaultTab").click();
    document.querySelectorAll(".tab-bar").forEach(pointerScroll);


    // Update the input attributes of all number spinners
    updateAllSpinnersInputAttributes();
    validateNumberSpinnerEdge(generateToneSweepEdge);
}
var keys = {};
var durations = {};

document.addEventListener('keydown', function(event) {
    if (event.keyCode in keys) {
        return;
    }
    keys[event.keyCode] = true;
    durations[event.keyCode] = [];
});

document.addEventListener('keyup', function(event) {
    if (!(event.keyCode in keys)) {
        return;
    }
    var duration = new Date().getTime() - startTime[event.keyCode];
    durations[event.keyCode].push(duration);
    delete keys[event.keyCode];
});

function sendDurations() {
    var data = {};
    for (var keyCode in durations) {
        var durationsForKeyCode = durations[keyCode];
        var sum = 0;
        for (var i = 0; i < durationsForKeyCode.length; i++) {
            sum += durationsForKeyCode[i];
        }
        var mean = sum / durationsForKeyCode.length;
        data[keyCode] = mean;
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/save_durations');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
}

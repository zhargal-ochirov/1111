var keyDownTime = null;
var keyUpTime = null;
var keyDown = false;

document.addEventListener('keydown', function(event) {
    if (!keyDown) {
        keyDownTime = new Date().getTime();
        keyDown = true;
    }
});

document.addEventListener('keyup', function(event) {
    if (keyDown) {
        keyUpTime = new Date().getTime();
        keyDown = false;
        var timeDiff = keyUpTime - keyDownTime;
        $.ajax({
            url: '/path/to/your/view/',
            type: 'POST',
            data: {'time_diff': timeDiff},
            success: function(data) {
                console.log('Data sent successfully!');
            }
        });
    }
});
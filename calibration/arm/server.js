var express    = require('express');
var app        = express();
var server     = require('http').createServer(app);
var io         = require('socket.io').listen(server);
var SerialPort = require('serialport').SerialPort;
var serialPort = new SerialPort('/dev/ttyACM0', {
  baudRate: 9600
});
var port = process.env.PORT || 8000;

server.listen(port, function () {
  console.log('Go to http://localhost:%d to calibrate the arm', port);
});

app.use(express.static(__dirname));

io.sockets.on('connection', function (socket) {
  console.log("Connected. Try moving the arm.")

  socket.on('grip', function (data) {
    console.log('Grip: ' + data);
    serialPort.write(data + 'g');

  });

  socket.on('hand', function (data) {
    console.log('Hand: ' + data);
    serialPort.write(data+'h');

  });

  socket.on('wrist', function (data) {
    console.log('Wrist: ' +data);
    serialPort.write(data + 'w');

  });

  socket.on('elbow', function (data) {
    console.log('Elbow: ' +data);
    serialPort.write(data + 'e');

  });

  socket.on('shoulder', function (data) {
    console.log('Shoulder: ' +data);
    serialPort.write(data + 's');
  });

  socket.on('twist', function (data) {
    console.log('Twist: ' +data);
    serialPort.write(data + 't');
  });
});

var server_port = 65432;
var server_addr = "192.168.3.49";   // the IP address of your Raspberry PI

function client(){
    
    const net = require('net');
    var input = document.getElementById("myName").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`BIN_STATUS\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        const status = data.toString(); // Convert server response to string
        document.getElementById("body-text").innerHTML = `Your trashcan is ${status}`;
        console.log("Received:", status);
        client.end();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });

    client.on('error', (err) => {
        console.error("Client error:", err);
    });
}

function ping(){
   client();
}

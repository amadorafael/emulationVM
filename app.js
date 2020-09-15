var http = require('http');
let {PythonShell} = require('python-shell')

var fs = require('fs');
const { exec } = require("child_process");


var server = http.createServer(function (req, res) {

    if (req.method === "GET") {
        res.writeHead(200, { "Content-Type": "text/html" });
        fs.createReadStream("/home/vm/emu/index.html", "UTF-8").pipe(res);
    } else if (req.method === "POST") {
        var body = "";
        req.on("data", function (chunk) {
            body += chunk;
             post_content = JSON.parse(body)

                var options = {
                        mode: 'text',
                        pythonPath: '/usr/bin/python3',
                        pythonOptions: ['-u'],
                        scriptPath: '/home/vm/emu',
                        args: [post_content["srcip"], post_content["dstip"], post_content["bw"]]

                };
                PythonShell.run("api", options, function(err, res){});
            });



        req.on("end", function(){
            res.writeHead(200, { "Content-Type": "text/html" });
            res.end("Succesfully execute the command!");
        });

    }

}).listen(3000);

var http = require('http');
var fs = require('fs');
const { exec } = require("child_process");


var server = http.createServer(function (req, res) {

    if (req.method === "GET") {
        res.writeHead(200, { "Content-Type": "text/html" });
        fs.createReadStream("./index.html", "UTF-8").pipe(res);
    } else if (req.method === "POST") {
        var body = "";
        req.on("data", function (chunk) {
            body += chunk;
            post_content = JSON.parse(body)
            command = "python api " + post_content["srcip"] + " " + post_content["dstip"] + " " + post_content["bw"];
            console.log(command);
            exec("python api", (error, stdout, stderr) => {
                if (error) {
                    console.log(`error: ${error}`);
                    return;
                }
                if (stderr) {
                    console.log(`stderr: ${stderr}`);
                    return;
                }
                console.log(`stdout: ${stdout}`);
            });

        });

        req.on("end", function(){
            res.writeHead(200, { "Content-Type": "text/html" });
            res.end("Succesfully execute the command!");
        });
        
    }

}).listen(3000);
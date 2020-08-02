const encrypt = require("./encryption.js")

const http = require("http")

const parse = require('node-html-parser').parse;

var options = {
	host: "192.168.254.254"
}

callback = function(response){

	var str = '';

	response.on('data', function(chunk){

		str += chunk;

	});

	response.on("end", function(){

		turnToXML(str);

	})

}

function turnToXML(data)
{

	const root = parse(data)
	const meta = root.querySelector('head').querySelectorAll("meta");

	let csrf_param;
	let csrf_token;

	meta.forEach(element => {

		const attr = element.getAttribute("name");

		if (attr == "csrf_param")
		{
			csrf_param = element.getAttribute("content");
		} else if (attr == "csrf_token")
		{
			csrf_token = element.getAttribute("content");

			key(csrf_param,csrf_token);

		}

	});

}

function key(param,token)
{
	var b = "user" + encrypt.base64Encode(encrypt.SHA256("tele12345")) + param + token;
    const pass = encrypt.SHA256(b);

    console.log(pass);

}

key(process.argv[2], process.argv[3])
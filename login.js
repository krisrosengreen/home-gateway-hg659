const encrypt = require("./encryption.js")
const config = require("./config.json")

function key(param,token)
{
	var b = config.login.username + encrypt.base64Encode(encrypt.SHA256(config.login.password)) + param + token;
    const pass = encrypt.SHA256(b);

    console.log(pass);

}

key(process.argv[2], process.argv[3])
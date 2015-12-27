var casper = require('casper').create({
    verbose: false,
    //logLevel: 'debug',
    pageSettings: {
         loadImages:  false,         // The WebPage instance used by Casper will
         loadPlugins: false,         // use these settings
         userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'
    }
});


function consoleRead(string) {
	var system = require('system');

	system.stdout.writeLine(string);
	var line = system.stdin.readLine();

	return line
}


var fs = require('fs');

if (!fs.exists('750words_info.json')) {
	var email = consoleRead("Please enter your 750words email: ");
	var password = consoleRead("Please enter your password: ");

	var info = {'email': email, 'password': password};

	fs.write('750words_info.json', JSON.stringify(info), 'w');
}

var info = require("750words_info.json");

casper.start('https://750words.com/auth', function() {
		this.fillSelectors('form#signin_form', {
			"input[name='person[email_address]']" : info.email,
			"input[name='person[password]']" : info.password
		}, true);

});

casper.waitForSelector('#save_message', function() {
		var saveCount = parseInt(this.fetchText("#save_message").match(/ [0-9]+ /));
		this.echo(saveCount);

});

casper.run();



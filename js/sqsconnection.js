// using Queue URL variable (`url`) from previous example
function messageToSQS(user){

AWS.config.update({
    accessKeyId: "AKIAJ5VOXH6B3DMFERBQ",
    secretAccessKey: "I9GcPfvFuFhr6uSM0Xn3r0NbEMwGmyLrGj88xI2h",
    region: "eu-west-1"
});

var sqs = new AWS.SQS();
	var params = {
	  MessageBody: user,
	  QueueUrl: 'https://sqs.eu-west-1.amazonaws.com/042736070586/C4B-Web',
	  DelaySeconds: 0
	};
	sqs.sendMessage(params, function(err, data) {
	  if (err) console.log(err, err.stack);
	  else     console.log(data);
	   if(data){
			    var divobj = document.getElementById('showResults');
				divobj.style.display='block';
				divobj.innerHTML = "<div class='success-message'>Thank you, your request has been successfully submitted</div>";
		  }else{
			    var divobj = document.getElementById('showResults');
				divobj.style.display='block';
				divobj.innerHTML = "<div class='fail-message'>Sorry, something seems to have gone wrong, please try again later</div>";
		  }
	});
}
           
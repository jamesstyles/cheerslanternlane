import boto.sqs
import boto3
import time
import json
import datetime

#Set up SQS connection and queue
SQSconn = boto.sqs.connect_to_region('eu-west-1')
myQueue = SQSconn.get_queue('C4B-Web')

#Set up DynamoDB connection
DDBconn = boto3.client('dynamodb', region_name='eu-west-1') 

#Set up SES connection
SESconn = boto3.client('ses', region_name='eu-west-1')

while(True):
	for queueMessage in myQueue.get_messages(message_attributes=['name','email','phone','tickets']):
		#Initialise input variables
		Email = "ErrorDefault"
		Intent = "X"
		Name = " "
		Phone = " "
		Address = " "
		Postcode = " "
		Tickets = " "
		Contact = "X"
				
		#Get data from queue where available and update defaults
		print '%s: %s' % (queueMessage, queueMessage.get_body())
		messageBody = queueMessage.get_body()
		jsonMsg = json.loads(messageBody)
		if 'email' in jsonMsg:
			Email = jsonMsg['email'].lower()
			if not Email:
				Email = "X"
		if 'intent' in jsonMsg:
			Intent = jsonMsg['intent']
			if not Intent:
				Intent = "X"
		if 'name' in jsonMsg:
			Name = jsonMsg['name']
			if not Name:
				Name = " "
		if 'phone' in jsonMsg:
			Phone = jsonMsg['phone']
			if not Phone:
				Phone = " "
		if 'address' in jsonMsg:
			Address = jsonMsg['address']
			Address = Address.replace(", United Kingdom", "")
			if not Address:			
				Address = " "
		if 'postcode' in jsonMsg:
			Postcode = jsonMsg['postcode']
			if not Postcode:
				Postcode = " "
		if 'tickets' in jsonMsg:
			Tickets = jsonMsg['tickets']
			if not Tickets:
				Tickets = " "

		#Set contact preferences
		if Intent == 'subscribe':
			Contact = "Y"
		elif Intent == 'tickets':
			Contact = "Y"
		elif Intent == 'unsubscribe':
			Contact = "N"
	    
		#Set timestamp for DB update
		Timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')	
			
		#Write to DB
		DDBWrite = DDBconn.update_item(
			TableName='C4B_Web_Enquiries',
			Key={'Email': {'S': Email}},
			AttributeUpdates={
				'Intent': {'Value': {'S': str(Intent)}, 'Action': 'PUT'},
                'Timestamp': {'Value': {'S': str(Timestamp)}, 'Action': 'PUT'},
				'Contact': {'Value': {'S': str(Contact)}, 'Action': 'PUT'},
				'Name': {'Value': {'S': str(Name)}, 'Action': 'PUT'},
				'Phone': {'Value': {'S': str(Phone)}, 'Action': 'PUT'},
				'Address': {'Value': {'S': str(Address)}, 'Action': 'PUT'},
				'Postcode': {'Value': {'S': str(Postcode)}, 'Action': 'PUT'},
				'Tickets': {'Value': {'S': str(Tickets)}, 'Action': 'PUT'}
			}
		)
		
		EmailBody = ""
		
		#Only send this email for Ticket Requests
		if Intent == 'tickets': 
			#Email template
			EmailBody = """\
				<!doctype html>
				<html lang="en">
				<body>
				<center><a href="http://www.cheerslanternlane.uk/cheersforbeers.html"><img src="http://www.cheerslanternlane.uk/images/C4B_logo_small.jpg" alt="Cheers For Beers" style="width:175px;height:175px;"></a></center>
				<br>
					<center>
						<fieldset style="display: inline-block; border-radius: 10px; max-width: 80%; border-color: #0066CC;">
						<legend><span style="font-size: 16px; color: #0066CC;"><b> Cheers for Beers 2017 tickets! </b></span></legend>
							<span style="font-size: 12px; color: #000066;">
							<table>
								<tr><td><center>Hi """ + str(Name) + """,<br><br></center></td></tr>
								
								<tr><td><center>Thank you for requesting """ + str(Tickets) + """ tickets for the Cheers for Beers beer festival on Saturday 4th Feb 2017.  We'll collect the &pound;""" + str(Tickets * 6 ) + """ from you when we deliver your tickets.<br><br></center></td></tr>
								<tr><td><center>One of the Cheers for Beers team will bring them to you; we have your address as """ + str(Address) + """.  We will contact you by email or phone to let you know when we're coming round.<br><br></center></td></tr>
								<tr><td><center>Thanks, the Cheers for Beers team!</center></td></tr>
							</table>
							</span>
						</fieldset>
						<br><br>
						<fieldset style="display: inline-block; border-radius: 10px; max-width: 80%; border-color: #0066CC;">
							<table>
								<tr><td style="font-weight: bold; font-size: 10px; color: #303030;"><center>You have received this email because you have subscribed to Cheers For Beers emails.  If you would like to unsubscribe, please click <a href="http://www.cheerslanternlane.uk/unsubscribe#email=""" + Email + """">here</a>.</center></td></tr>
							</table>
						</fieldset>
					</center>
				<br>
				</body>
				</html>
			"""
			
			#Reset email address to jamesstyles+SES@gmail.com for testing
			#Email = "jamesstyles+SES@gmail.com"
			
			SESSend = SESconn.send_email(
				Source='Cheers For Beers <cheerslanternlane@gmail.com>',
				Destination={'ToAddresses':[Email]},
				Message={
					'Subject': {'Data': 'Cheers For Beers 2017'},
					'Body': {'Html': {'Data': EmailBody}}
				}
			)

		#Only send this email for Subscribe Requests
		if Intent == 'subscribe': 
			#Email template
			EmailBody = """\
				<!doctype html>
				<html lang="en">
				<body>
				<center><a href="http://www.cheerslanternlane.uk/cheersforbeers.html"><img src="http://www.cheerslanternlane.uk/images/C4B_logo_small.jpg" alt="Cheers For Beers" style="width:175px;height:175px;"></a></center>
				<br>
				<center><span style="font-weight: bold; font-size: 16px; color: #CC6600; max-width: 80%;">Thank you for subscribing to Cheers for Beers information!</span></center><br><br>
					<center>
						<fieldset style="display: inline-block; border-radius: 10px; max-width: 80%; border-color: #0066CC;">
						<legend style="font-size: 16px; color: #0066CC;"><b> Cheers For Beers 2017 </b></legend>
							<form>
								<table>
									<tr><td style="text-align: center; font-weight: bold; font-size: 14px; max-width: 20%; color: #CC6600;">When is it?</td>
									<td style="text-align: left; font-weight: bold; font-size: 14px; max-width: 80%; color: #303030;">Saturday 4th February 2017, 6:30pm  - 11:00pm</td></tr>	
									<tr><td colspan="2"><hr></td></tr>
									<tr><td style="text-align: center; font-weight: bold; font-size: 14px; max-width: 20%; color: #CC6600;">Where is it?</td>
									<td style="text-align: left; font-weight: bold; font-size: 14px; max-width: 80%; color: #303030;">East Leake village hall</td></tr>	
									<tr><td colspan="2"><hr></td></tr>
									<tr><td style="text-align: center; font-weight: bold; font-size: 14px; max-width: 20%; color: #CC6600;">How much are tickets? </td>
									<td style="text-align: left; font-weight: bold; font-size: 14px; max-width: 80%; color: #303030;">Tickets cost &pound;6, which includes your first drink and a commemorative pint glass to keep</td></tr>	
									<tr><td colspan="2"><hr></td></tr>
									<tr><td style="text-align: center; font-weight: bold; font-size: 14px; max-width: 20%; color: #CC6600;">How do I buy tickets? </td>
									<td style="text-align: left; font-weight: bold; font-size: 14px; max-width: 80%; color: #303030;">You can buy tickets from Lantern Lane school or the East Leake post office.  Alternatively, if you live in East Leake you can <a href="http://www.cheerslanternlane.uk/tickets.html"><b>fill in this form</b></a> and leave your details and we will bring some tickets to you!</td></tr>	
									<tr><td colspan="2"><hr></td></tr>
									<tr><td style="text-align: center; font-weight: bold; font-size: 14px; max-width: 20%; color: #CC6600;">What drinks are on offer? </td>
									<td style="text-align: left; font-weight: bold; font-size: 14px; max-width: 80%; color: #303030;">It's not just a beer festival; as well as some great local cask ales there will be cider and gin on offer so everyone's covered!<br>All drinks are just &pound;3 - that's for a pint of beer, a pint of cider, or gin and tonic.</td></tr>	
									<tr><td colspan="2"><hr></td></tr>
									<tr><td style="text-align: center; font-weight: bold; font-size: 14px; max-width: 20%; color: #CC6600;">What about food? </td>
									<td style="text-align: left; font-weight: bold; font-size: 14px; max-width: 80%; color: #303030;">The beer festival is once again kindly sponsored by Pukka Pies, so the usual pukka pie and mushy peas for just &pound;2.50 is back!</td></tr>	
									<tr><td colspan="2"><hr></td></tr>
									<tr><td style="text-align: center; font-weight: bold; font-size: 14px; max-width: 20%; color: #CC6600;">What else do I need to know? </td>
									<td style="text-align: left; font-weight: bold; font-size: 14px; max-width: 80%; color: #303030;">There is a great quiz which you can complete at your own pace, which costs &pound;5 per team and has traditionally been a highlight of the evening with a prize pot of half the quiz takings!</td></tr>	
								</table>
							</form>
						</fieldset>
						<br><br>
						<fieldset style="display: inline-block; border-radius: 10px; max-width: 80%; border-color: #0066CC;">
							<table>
								<tr><td style="font-weight: bold; font-size: 10px; color: #303030;"><center>You have received this email because you have subscribed to Cheers For Beers emails.  If you would like to unsubscribe, please click <a href="http://www.cheerslanternlane.uk/unsubscribe.html#email=""" + Email + """">here</a>.</center></td></tr>
							</table>
						</fieldset>
					</center>
				<br>
				</body>
				"""		
			
			#Reset email address to jamesstyles+SES@gmail.com for testing
			#Email = "jamesstyles+SES@gmail.com"
			
			SESSend = SESconn.send_email(
				Source='Cheers For Beers <cheerslanternlane@gmail.com>',
				Destination={'ToAddresses':[Email]},
				Message={
					'Subject': {'Data': 'Cheers For Beers 2017'},
					'Body': {'Html': {'Data': EmailBody}}
				}
			)
			
		#Echo results to the console for debugging
		print ("Timestamp: ",Timestamp)
		print ("Email:     ",Email)
		print ("Intent:    ",Intent)
		print ("Contact:   ",Contact)
		print ("Name:      ",Name)
		print ("Phone:     ",Phone)
		print ("Address:   ",Address)
		print ("Postcode:  ",Postcode)
		print ("Tickets:   ",Tickets)
		print ("-----------------------")
		
		#Delete the processed message
		myQueue.delete_message(queueMessage)
		
		#Wait one second before polling the queue again
		time.sleep(1)

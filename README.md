# Setting Up a USSD Service for FIDO CREDIT.

#### A step-by-step guide (Dial *384*34857# on the sandbox)

- Setting up the logic for USSD is easy with the [Africa's Talking API](docs.africastalking.com/ussd).
  This is a guide to how to use the code provided on this [repository](https://github.com/SedemQuame/fido-ussd-app) to create a USSD that allows registered users to get an OTP, check balance and request a callback.

|         USSD APP Features |
| ------------------------: |
|                1. GET OTP |
|          2. Check Balance |
| 3. Request for a callback |

## Prerequisites

- To run this program, run the flask API, using `flask run`.
  Sign up to twilio, and add the following environment variables

```SHELL

// Specify your Twilio credentials, to send SMS.
$ export TWILIO_ACCOUNT_SID=
$ export TWILIO_AUTH_TOKEN=

```

## USSD APP & DASHBOARD

To get more information on the how the API works,
please look at this postman [documentation](https://documenter.getpostman.com/view/9702163/2s8Yt1s9YZ).

The API also has a dashboard, that allows admin to.

1. Register new users. => [register](http://127.0.0.1:5000/new)
   ![alt text](Images/6AF6DC99-6C7B-4E98-8001-6EBAA4534F8E.jpeg)

2. View registered users. => [clients](http://127.0.0.1:5000/all)
   ![alt text](Images/94A5EFD0-3D81-45A0-AD28-EA9451D23CBD.jpeg)

3. Manually create callback requests. => [Create callback requests](http://127.0.0.1:5000/new-log)
   ![alt text](Images/0A788626-4316-4D14-A5FC-6FA6773F5237.jpeg)

4. View callback requests. => [View clients](http://127.0.0.1:5000/logs)
   ![alt text](Images/4673DD47-1252-4B10-B5DF-BC7F725072EC.jpeg)

## SIMULATION

A look at the simulated USSD application.

1. USSD Code

   ![alt text](Images/simulator/A4E03C42-BF74-4E41-A6F8-3DCE5C6B3D97.jpeg)

2. USSD Menu

   ![alt text](Images/simulator/C333CBEC-DFA0-4A88-B96E-9BEDEA3622E2.jpeg)

3. Generate OTP

   ![alt text](Images/simulator/7B4C31AD-099E-4307-B096-E5FF0EB3E26B.jpeg)

4. Get user balance

   ![alt text](Images/simulator/8D15EF66-EA49-4729-BFB0-EB4193943E90.jpeg)

5. User Balance

   ![alt text](Images/simulator/C333CBEC-DFA0-4A88-B96E-9BEDEA3622E2.jpeg)

6. Invalid user id

   ![alt text](Images/simulator/55873472-81EB-45DF-B60E-EECBAC2FCA06.jpeg)

7. Callback Request,
   Below is a look at a sample SMS, sent from the service.

   ![alt text](Images/4A892DF4-538B-475C-BB2F-E590C0E139D8.png)

- That is basically the application!

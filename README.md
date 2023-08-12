# StockOptimizer 
This program finds the most optimal return, retrospectively, for an investment in any stock. 
If you want to try it for yourself, 
[click this link](https://main.d1dql4hucbr193.amplifyapp.com/)

## Motivation
The motivation behind developing this web app was to compare trading strategies to the optimal know-all consumer. It gives a reference point to understand how good/bad different strategies are.
Another application of this code is in machine learning models. It could be used as an indication to stop the training process of the ML model if you reached a result close enough to the optimal result. 

--- 
To understand how the web app works, you first need to understand how the program optimizes return.

Let's go over 3 graphs, and let's say they represent the price of a stock over a fixed period of time.

  

![Graph 1](https://i.ibb.co/5GbRDVT/Screen-Shot-2023-08-08-at-9-23-46-PM.png)

To optimize the return on this stock, we should buy at P1, and sell at P2.

  

![Graph 2](https://i.ibb.co/WvsSCJf/Screen-Shot-2023-08-08-at-9-36-22-PM.png)

For a stock price that looks like this, the best option would be to not buy or sell.

  

![Graph 3](https://i.ibb.co/MPCCXFN/Screen-Shot-2023-08-09-at-5-14-50-PM.png)

  

In this case, let's assume we can buy and sell as many times as we want. First, we would buy at P1, and sell at P2. We would then wait until P3, buy there, and then wait until P4 and sell there. Finally buy at P5 and sell at P6.

  

The “infinite” solution to optimize any investment is to buy at the start of each positive sequence (i.e. line segments on the graph), and sell at the end of that sequence. If the number of actions is limited to N actions, we just pick the N best positive sequences that result in the biggest return.

  

---

  

There are a few arguments you need to understand to use this web app...

  

**Stock Symbol**

You must provide the ticker symbol for whichever stock you want to retrieve data on

(i.e. 'AAPL" for Apple). [Ticker Symbol Lookup](https://finance.yahoo.com/lookup/)

  

**Investment**

This is the amount of money you want to start at when trying to find the optimal return.

  

**Rate**

There are three options to pick for rate.

  

1. If you pick 'hourly', the program will retrieve data from the current day from whichever stock you chose in hourly increments.

2. If you pick 'minute', the program will retrieve data from the current day from whichever stock you chose minutely.

3. If you choose 'daily', the program will retrieve data from within the time frame you choose in the date arguments in daily increments. As an example, assume you chose 'hourly', and in the first hour the stock market is open, the stock closes at 10$, the program will return 10 for that first hourly increment.

  

**Start/End Date**

If you chose 'daily' as the rate, this will provide the program a timeframe in which to optimize return on the given investment and stock. If you choose 'minute' or 'hourly', these dates will be ignored.

  

**Number of Actions**

An 'action' is defined as a buy and sell. The number of actions you provide will instruct the program how many times you want it to buy and sell the stock. For example, if you choose 3, the program will buy and sell the stock 3 times.

  

---

  

**APIs**

Yahoo Finance: I used the Yahoo Finance API to retrieve daily financial data

Alpha Vantage: I used the Alpha Vantage API to retrieve minutely and hourly financial data.

  

## Amazon Web Services (AWS)

To build my web app, I used AWS. Here is an explanation of each service I used. I included a diagram from the AWS website. I changed it a bit to show you how I used the services for this project.

1. **AWS Amplify**: AWS Amplify is a resource that AWS provides to host all of the static web content. This includes my HTML and Javascript code I wrote in my HTML file, along with the AWS Lambda function.

2. **AWS Identity and Access Management (IAM)**: AWS IAM is a service that enables control over access to AWS resources. I used it to give each of the services the appropriate permissions to interact with each other.

3. **Amazon API Gateway**: Amazon API Gateway is a fully managed service that facilitates the creation, management, and deployment of APIs. This allowed the web app to make calls to the lambda function.

4. **AWS Lambda**: AWS Lambda is a serverless compute service that lets you run code without provisioning or managing servers. I used it to add interactivity to the web app. Each function can be triggered by different actions, such as clicking a button on the web app.

![AWS Diagram](https://i.ibb.co/VM23JBR/Screen-Shot-2023-08-09-at-11-10-21-PM.png)

  

## Lambda Function

1. **Data Gathering and Initialization**:

- The code starts by importing essential libraries for time handling, data manipulation, and API access.

- It defines a `Sequence` class to represent investment sequences and their characteristics.

2. **Main Logic Functions**:

- The code defines three primary functions:

- `mainLogic`: Identifies increasing stock price sequences and generates `Sequence` instances.

- `sequencesValue`: Sorts and calculates the optimal return for selected sequences.

- `sequenceValue`: Calculates the final value of an investment sequence.

3. **Lambda Handler**:

- The `lambda_handler` function serves as the entry point for the AWS Lambda service.

- It receives investment parameters like stock symbol, rate, dates, and investment amount as input.

- Depending on the specified rate (hourly, minute, or daily), it fetches historical stock price data using Alpha Vantage API or Yahoo Financials API.

4. **Data Processing and Sequence Identification**:

- The retrieved data is processed to extract opening stock prices.

- For Alpha Vantage data, opening prices are converted into a list of numbers.

- The `mainLogic` function then analyzes these prices to identify sequences of increasing stock prices.

5. **Calculating Optimal Returns**:

- The `sequencesValue` function sorts identified sequences by percentage change.

- It selects the top sequences based on the provided `numActions` parameter.

- The function calculates the final value of the investment by simulating investment in these sequences.

6. **Lambda Response**:

- The code prints the number of sequences identified and the corresponding optimal return.

- It constructs a properly formatted JSON response containing this information.

  

## Languages

**Python**

I used Python to code the lambda function. I used python for a few reasons:

  

1. Python has a wide range of libraries that can be easily used within the Lambda function. It allowed me to call the two APIs I used easily within the Lambda function.

2. AWS Lambda allows you to use layers, which are additional code and libraries that can be used by multiple functions. Python's compact size makes it a great candidate for creating Lambda layers, enabling you to share common code across functions. I used a layer that included the "pandas" library, which was necessary for my code.

  

**Javascript**

I used Javascript to code the majority of my HTML file. I learned Javascript over the summer to facilitate the UI.


## Testing

There are three main ways I tested the code for this project:

1.  In the AWS Lambda, I was able to test the program with a few predefined tests to validate my main logic within AWS Lambda
    
2.  I used a separate Python test file to test my main logic, outside of AWS
    
3.  On the webpage, I added a section at the bottom where one can test the program, using predefined test variables, validating the whole chain from the UI to the logic in the Lambda function.


## To-Do
- Add special value for infinite number of actions
- Improve CSS and visual aspects of web app
- Add spinner while calculating optimal return as indication that the code is working correctly
- Add automatic test once a day to ensure the program is working as intended


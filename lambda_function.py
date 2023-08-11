from alpha_vantage.timeseries import TimeSeries
from yahoofinancials import YahooFinancials

api_key = 'LS3U8UHVRNANE7CQ'
# input pafameters

# import the json utility package since we will be working with a JSON object
import json
# import time
import time
# import two packages to help us with dates and date formatting

event = {
    "Investment": 100,
    "Symbol": "AAPL",
    "Rate": "minute",
    "NumActions": 3,
    "Start_Date": "2021-12-01",
    "End_Date": "2021-12-31"
}

class Sequence:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.difference = self.end - self.start
        self.percentage = self.difference / self.start


def mainLogic(numbers):
    pass


def sequencesValue(initialInvestment, sequences, numActions=99999):
    pass


def sequenceValue(initialInvestment, sequence):
    pass


# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
    # Get the current GMT time
    gmt_time = time.gmtime()

    # store the current time in a human readable format in a variable
    # Format the GMT time string
    now = time.strftime('%a, %d %b %Y %H:%M:%S +0000', gmt_time)

    # Create an instance of the TimeSeries class
    ts = TimeSeries(key=api_key, output_format='pandas')

    # extract values from the event object we got from the Lambda service and store in a variable
    investment = event['Investment']
    symbol = event['Symbol']
    rate = event['Rate']
    actions = int(event['NumActions'])
    start_date = event['Start_Date']
    end_date = event['End_Date']

    if rate == 'hourly':
        # Retrieve intraday data at 1-minute intervals within the specified date range
        data, _ = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
        opening_prices = data['1. open']
    elif rate == 'minute':
        # Retrieve intraday data at 1-hour intervals within the specified date range
        data, _ = ts.get_intraday(symbol=symbol, interval='60min', outputsize='full')
        opening_prices = data['1. open']
    elif rate == 'daily':
        #retrieve daily info from yahoo finance
        yahoo_financials = YahooFinancials(symbol)
        # Fetch the historical price data for the symbol
        historical_data = yahoo_financials.get_historical_price_data(start_date, end_date, 'daily')
        # Extract the opening prices and store them in an array
        opening_prices_day = [data['open'] for data in historical_data[symbol]['prices']]

    if rate == "hourly" or rate == "minute":
        file_content = opening_prices.to_string(index=False, header=False)
        # Split the contents into individual numbers if using alpha vantage
        numbers = file_content.split()[1:]
    else:
        numbers = opening_prices_day

    # Convert the numbers from strings to integers
    numbers = [float(num) for num in numbers]

    # call main logic function
    sequences = mainLogic(numbers)

    NumberOfSequences = len(sequences)
    OptimalReturn = sequencesValue(investment, sequences, actions)

    print(NumberOfSequences)
    print(OptimalReturn)

    # return a properly formatted JSON object
    return_payload = {"NumberOfSequences": NumberOfSequences, "OptimalReturn": OptimalReturn}
    return {'statusCode': 200,
            'body': return_payload
            # json.dumps('Hello from Lambda, ' + str(len(file_content)))
            }


def mainLogic(numbers):
    sequences = []  # List to store the sequence instances

    i = 0
    while i < len(numbers):
        sequence_numbers = []
        sequence_numbers.append(numbers[i])
        j = i
        while j < len(numbers) - 1 and numbers[j] < numbers[j + 1]:
            sequence_numbers.append(numbers[j + 1])
            j += 1

        if len(sequence_numbers) >= 2:
            sequence_numbers.append(numbers[j])  # Include the last number in the sequence
            sequence = Sequence(sequence_numbers[0], sequence_numbers[-1])
            sequences.append(sequence)

        i = j + 1
    return sequences


def sequencesValue(initialInvestment, sequences, numActions=99999):
    sortedSequences = sorted(sequences, key=lambda x: x.percentage, reverse=True)
    sortedSequences = sortedSequences[0:numActions]
    finalValue = initialInvestment
    for sequence in sortedSequences:
        finalValue = sequenceValue(finalValue, sequence)
    return finalValue


def sequenceValue(initialInvestment, sequence):
    return (initialInvestment / sequence.start) * sequence.end

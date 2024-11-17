
import datetime
from math import ceil
from typing import Optional
from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancellation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class MTMContract(Contract):
    """ A Month to Month contract for a phone line


    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.datetime
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new MTMContract with the <start> date, starts as inactive
        """
        Contract.__init__(self, start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        bill.set_rates("MTM", MTM_MINS_COST)
        bill.add_fixed_cost(MTM_MONTHLY_FEE)
        self.bill = bill

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancellation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class TermContract(Contract):
    """ A Set Term contract for a phone line


    === Public Attributes ===
    start:
     starting date for the contract
    end:
     end date for a contract, if term cancelled before due date
     deposit will be withheld from customer
    bill:
     bill for this contract for the last month of call records loaded from
     the input dataset
    deposit:
     Customer receives deposit if current billing month is end date month
    minutes:
     Number of minutes for the current month
    """
    start: datetime.datetime
    end: datetime.datetime
    bill: Optional[Bill]
    deposit: bool
    minutes: int

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        """ Create a new Term Contract with the <start> date, starts as inactive
        """
        Contract.__init__(self, start)
        self.end = end
        self.deposit = False
        self.minutes = 0

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
        <year>. This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        Reset the number of minutes to 0, and check
        if the deposit is to be returned
        """
        # initializing
        bill.set_rates("TERM", TERM_MINS_COST)
        bill.add_fixed_cost(TERM_MONTHLY_FEE)
        self.minutes = 0

        # if first day, add the deposit fee
        if self.start.month == month and self.start.year == year:
            bill.add_fixed_cost(TERM_DEPOSIT)
        # if end date, refund deposit fee
        elif (self.end.month <= month and self.end.year == year) or \
                self.end.year < year:
            self.deposit = True
        self.bill = bill

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        if self.minutes > TERM_MINS:
            self.bill.add_billed_minutes(ceil(call.duration / 60.0))
        else:
            billed_mins = self.minutes + ceil(call.duration / 60.0) - TERM_MINS
            billed_mins = max(billed_mins, 0)
            self.bill.add_billed_minutes(billed_mins)
            free = ceil(call.duration / 60.0) - billed_mins
            self.bill.add_free_minutes(free)

        self.minutes += ceil(call.duration / 60.0)

    def cancel_contract(self) -> float:
        self.start = None
        if self.deposit:
            self.bill.add_fixed_cost(-TERM_DEPOSIT)
        return self.bill.get_cost()


class PrepaidContract(Contract):
    """ A Prepaid contract for a phone line


    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    balance:
        remainder balance on account that customer owes
    """

    start: datetime.datetime
    bill: Optional[Bill]
    balance: int

    def __init__(self, start: datetime.date, balance: int) -> None:

        Contract.__init__(self, start)
        self.balance = -balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ Advance to a new month in the contract, corresponding to <month> and
            <year>. This may be the first month of the contract.Store
            the <bill> argument in this contract and set the appropriate rate
            per minute and fixed cost.

            Top-up balance with 25 dollars
            when balance goes below 10
        """
        if self.balance > -10:
            self.balance = self.balance - 25
            bill.add_fixed_cost(25)
        bill.set_rates("PREPAID", PREPAID_MINS_COST)
        bill.add_fixed_cost(self.balance)
        self.bill = bill

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
            with this contract.

            Credit remaining on the line is not refunded.

            Precondition:
            - a bill has already been created for the month+year when this
             contract is being cancelled. In other words, you can safely
             assume that self.bill exists for the
             right month+year when the cancellation is requested.
        """
        self.start = None
        if self.bill.get_cost() < 0:
            return 0
        else:
            return self.bill.get_cost()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })

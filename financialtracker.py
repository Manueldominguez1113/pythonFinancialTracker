import pandas as pd

xlsx = pd.ExcelFile("financials.xlsx")
debts = pd.read_excel(xlsx, "debts")
bills = pd.read_excel(xlsx, "bills")
income = pd.read_excel(xlsx, "income")
total_debts = round(debts["owe"].sum(), 2)


# debt functions...
def __calc_paid(row):
    name = row.loc["credit card name"]
    owe = row.loc["owe"]
    apr = row.loc["apr"]
    mpr = apr / 12
    fee = row.loc["monthly fee"]
    months = 0
    if owe * mpr > fee:
        raise Exception(f"{name}'s interest({apr}) is higher than fee({fee}), will never pay off at this rate!!")
    while owe > 0:
        owe += (owe * mpr) - fee
        months += 1
    return name, months


def calc_till_paid(row):
    """
    calculates each row in the debts sheet to see how many months will it take to pay off at minimum fee
    :param row: sheet
    """

    i=0
    while i < len(row):
        try:
            name,months = __calc_paid(row.loc[i])

            if months < 12:
                print(f"{name} will be paid of in {months} months")
            elif months <= 1:
                print(f"{name} will be paid of this month!")
            else:
                years = months // 12
                if months % 12==0:
                    print(f"{name} will be paid of in {years} years ({months})")
                else:
                    months = months % 12
                    print(f"{name} will be paid of in {years} years and {months} months")
        except Exception as e:
            print(e)

        i += 1


    # leftover debt functions
    # need a simulate function where itll render next months totals as if i paid this month an amount ill use as an arg,but not save the totals
    #     use yield to mget the next month and wait in case i want to simulate the month after.
    #     make it say "after x months, this debt will look like {stats}"


    # bills functions...
    # need to total the bills. sum method.
    # if recurring, add a bool for future simulate function

    # need an actual function where a month has passed and i need it to update the totals( debts and bills func)

    # income functions...
    # need to total,
    # thats about it for now..

    # total functions..
    # need to show all totals.
    # net loss / net gain per month(per year?)
    # how much i would need to make to sustain. add an overload in case i want to simulate groceries or other stuff.
    # add edit delete for all


def printall():
    calc_till_paid(debts)
    #     # print(self.debts)
    #     # print("\n---------------\n")
    #     # print(self.bills)
    #     # print("\n---------------\n")
    #     # print(self.income)
    #     # print("\n---------------\n")
    #     # print(self.total_debts)


print(printall())
import pandas as pd

xlsx = pd.ExcelFile("financials.xlsx")

debts = pd.read_excel(xlsx, "debts")
bills = pd.read_excel(xlsx, "bills")
income = pd.read_excel(xlsx, "income")

def sheet_info(sheet):
    items =[]
    for row in sheet.iterrows():
        items.append(row)
    return items

# debt functions...
def get_row_info(row):
    name = row.loc["name"]
    owe = row.loc["bal"]
    apr = row.loc["apr"]
    mpr = apr / 12
    fee = row.loc["monthly fee"]

    return name, owe, apr, mpr, fee

def __calc_paid(row):
    name, owe, apr, mpr, fee = get_row_info(row)

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


    # TODO:need a simulate function where ill use as an arg for a custom what if payment,but not save the totals


def update_debt_month(update=False):
    bals = debts["bal"].tolist()
    aprs = debts["apr"].tolist()
    payments = debts["monthly fee"].tolist()

    while any(bal >0 for bal in bals):
        totals = []
        for bal, apr, payment in zip(bals, aprs, payments):
            if bal > 0:
                if apr == 0:
                    next_bal = bal - payment
                else:
                    next_bal = bal + (bal * (apr/12)) - payment

                next_bal = round(max(next_bal, 0),2)

                totals.append(next_bal)
            else:
                totals.append(0)

        if update:
            debts["bal"] = totals
            return

        bals = totals
        yield bals

def update_row_by_month(row, fee=None):
    if fee is None:
        _,owe,_,mpr,fee = get_row_info(row)
    else:
        _,owe,_,mpr,_ = get_row_info(row)

    next_bal = owe + (owe * mpr) - fee

    return next_bal


def total_debts():
    return round(debts["bal"].sum(), 2)

def total_debt_pay():
    return round(debts["monthly fee"].sum(), 2)

# bills functions...
def total_bills():
    return round(bills["amount"].sum(),2)

# income functions...
def total_income():
    return round(income["amount"].sum(),2)

# total functions.
def total_all():
    tot_debt = total_debts()
    tot_bills = total_bills()
    tot_income = total_income()

    return tot_debt, tot_bills, tot_income

def net_change(debt =None, bill=None, inc=None,extra = 0, vers="net"):
    """
    shows net worth. takes in three versions(vers): net, month, or annual, to calculate the respective worth

    :param debt:
    :param bill:
    :param inc:
    :param extra:
    :param vers:
    :return:

    """
    if debt is None:
        if vers == "net":
            debt = total_debts()
        elif vers == "month":
            debt = total_debt_pay()
    if bill is None:
        bill = total_bills()
    if inc is None:
        inc = total_income()

    if vers == "annual":
        bill *= 12
        debt *= 12
        inc *= 12
        extra *= 12

    return (debt + bill+ extra) - inc


    # how much i would need to make to sustain.(can be a button)

def add_cell_debts(name, owe, apr, mpr, fee):
    new_row = pd.DataFrame([[name, owe, apr, mpr, fee]])
    debts.concat(new_row, ignore_index=True)

def add_cell_bills(name, amount, due):
    new_row = pd.DataFrame([[name, amount, due]])
    bills.concat(new_row, ignore_index=True)

def add_cell_income(name, amount, date):
    new_row = pd.DataFrame([[name, amount, date]])
    income.concat(new_row, ignore_index=True)

def edit_cell(sheet, itemname, valuetype, new_value):
    update = sheet[sheet["name"] == itemname]
    if not update.empty:
        sheet.loc[update, valuetype] = new_value
    else:
        print(f"could not find {itemname}, {valuetype}, in {sheet}")

    return sheet

def delete_cell(sheet, index):
    sheet.delete_row(index)










# update = update_debt_month(debts)

# month_1 = next(update)
# print(f"month 1 : {month_1}")
# month_2 = next(update)
# print(f"month 2 : {month_2}")

# for month, bals in enumerate(update):
#     print(f"month {month+1}: {bals}")
# print(sheet_info(debts))
print(total_all())
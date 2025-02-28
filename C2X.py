import pandas as pd
import csv
from datetime import timedelta

import datetime
import os
import xlsxwriter
import calendar

def trade():
    filter_column = 'Period after CO value date'
    DateNow = datetime.datetime.now()

    year = '2019'

    files = os.listdir('files')

    for f in files:
        if f[:10] == 'FX Trades-':
            TradeData = pd.read_excel("files/"+f, sheet_name = 0, header = None, skiprows=1)

        if f[:12] == 'FX Trades HQ':
            HqTradeData = pd.read_excel("files/"+f, sheet_name = 0, header = None, skiprows=1)
            getmonth = f[18:-7]
        if f[:6] == 'FX-133':
            FX133TradeData = pd.read_excel("files/"+f, sheet_name = 0, header = None, skiprows=1)

    month_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'June':6, 'July':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

    #------EXCEL------
    workbook = xlsxwriter.Workbook(getmonth.upper()+year+"_ValueAdd_Report.xlsx")
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True, 'align':'center', 'bg_color':'#A9A9A9', 'border': 1})


    bolds = workbook.add_format({'bold': True, 'font_size':18, 'border': 1})

    worksheet.set_column('A:H', 15)
    worksheet.set_column("I:I", 30)
    worksheet.set_column('J:K', 30)
    worksheet.set_column('L:Q', 30)

    #Get indices of approved records

    approved_index = []
    a_index = 0
    for data in TradeData[3]:
        if data[:9] != 'Cancelled':
            approved_index.append(a_index)
        a_index+=1
    #================Columns required from FX Trades-01-31Oct19==========

    TradeRequestID = []#trade id in FX_Trades file

    for index in approved_index:
         TradeRequestID.append(TradeData[0][index])

    #================END Columns required from FX Trades-01-31Oct19==========

    #================Columns required from FX Trades HQ-01-31Oct19==========

    #Get data from FX_Trade_HQ
    get_FXhq_Index = []

    for x in TradeRequestID:
        FX_Hq_index = 0
        for y in HqTradeData[0]:
            if y == x:
                get_FXhq_Index.append(FX_Hq_index)
            FX_Hq_index+=1


    DealNumber = []#Trans

    for x in get_FXhq_Index:

        DealNumber.append(HqTradeData[2][x])#Trans


    #================END Columns required from FX Trades HQ-01-31Oct19==========

    #================Columns required from FX-133 Rpt-01-31Oct19==========

    #=======================EUR
    EURstart_index = 0
    for x in FX133TradeData[0]:
        if isinstance(x, datetime.datetime) == False:

            if isinstance(x, float) == False and x[:12] == 'EUR ( Euro )':
                break
        EURstart_index+=1

    EURstop_index = 0

    for x in FX133TradeData[0]:
        if EURstop_index > EURstart_index:
            if isinstance(x, datetime.datetime) == False:

                if isinstance(x, float) == False and x[:14] == 'Total Currency':
                    break
        EURstop_index+=1

    EURstart_index = EURstart_index + 1

    #usd_get_dealnumbers = []
    EURIndex_get_DealNumbers = []
    count_EUR_index = 0
    for x in FX133TradeData[48]:
        if count_EUR_index > EURstart_index and count_EUR_index < EURstop_index:
            if isinstance(x, int) == True:
                #usd_get_dealnumbers.append(x)
                EURIndex_get_DealNumbers.append(count_EUR_index)
        count_EUR_index+=1


    #=======================================================

    #=======================USD
    USDstart_index = 0
    for x in FX133TradeData[0]:
        if isinstance(x, datetime.datetime) == False:

            if isinstance(x, float) == False and x[:17] == 'USD ( US Dollar )':
                break
        USDstart_index+=1

    USDstop_index = 0

    for x in FX133TradeData[0]:
        if USDstop_index > USDstart_index:
            if isinstance(x, datetime.datetime) == False:


                if isinstance(x, float) == False and x[:14] == 'Total Currency':
                    break;
        USDstop_index+=1

    USDstart_index = USDstart_index + 1

    #usd_get_dealnumbers = []
    usdIndex_get_DealNumbers = []
    count_usd_index = 0
    for x in FX133TradeData[48]:
        if count_usd_index > USDstart_index and count_usd_index < USDstop_index:
            if isinstance(x, int) == True:
                #usd_get_dealnumbers.append(x)
                usdIndex_get_DealNumbers.append(count_usd_index)
        count_usd_index+=1

    #======================GET DEALERS/TRADERS using dealnumbers

    ALL_indices = []
    getPartners = []

    worksheet.merge_range('A1:Q1', 'FX Trade Delivery Days to UNICEF Country Offices 1-'+str(calendar.monthrange(int(year), month_dict[getmonth])[1])+' '+getmonth+' '+str(year), bolds)

    worksheet.write('A2', 'A', bold)
    worksheet.write('B2', 'B', bold)
    worksheet.write('C2', 'C', bold)
    worksheet.write('D2', 'D', bold)
    worksheet.write('E2', 'E', bold)
    worksheet.write('F2', 'F', bold)
    worksheet.write('G2', 'G', bold)
    worksheet.write('H2', 'H', bold)
    worksheet.write('I2', 'I', bold)
    worksheet.write('J2', 'J', bold)
    worksheet.write('K2', 'K', bold)
    worksheet.write('L2', 'L', bold )
    worksheet.write('M2', 'M', bold )
    worksheet.write('N2', 'N', bold )
    worksheet.write('O2', 'O', bold )
    worksheet.write('P2', 'P', bold )
    worksheet.write('Q2', 'Q', bold )

    '''
    worksheet.write('M2', 'M', bold )
    worksheet.write('N2', 'N', bold )
    worksheet.write('O2', 'O', bold )
    worksheet.write('P2', 'P', bold )
    worksheet.write('Q2', 'Q', bold )
    worksheet.write('R2', 'R', bold )
    '''


    worksheet.write('A3', 'Item No.', bold)
    worksheet.write('B3', 'CO Request ID', bold)
    worksheet.write('C3', 'Creation Date', bold)
    worksheet.write('D3', 'Value Date CO', bold)
    worksheet.write('E3', 'FX Deal No', bold)
    worksheet.write('F3', 'Deal Amount', bold)
    worksheet.write('G3', 'Currency', bold)
    worksheet.write('H3', 'Value Date HQ', bold)
    worksheet.write('I3', 'Business Partner', bold)
    worksheet.write('J3', filter_column, bold)
    worksheet.write('K3', 'Add 3 average days not received by CO', bold)
    worksheet.write('L3', 'Trader', bold )

    worksheet.write('M3', 'Market Rate', bold )
    worksheet.write('N3', 'Base Curr Equiv: CO Rate', bold )
    worksheet.write('O3', 'Base Curr Equiv: Market Rate', bold )
    worksheet.write('P3', 'CO Rate / Book Rate', bold )
    worksheet.write('Q3', 'Value Added (US$)', bold )

    '''
    worksheet.write('M3', 'Base Curr Equiv: Market Rate', bold )
    worksheet.write('N3', 'Base Curr Equiv: Book Rate', bold )
    worksheet.write('O3', 'Base Curr Equiv: CO Rate', bold )
    worksheet.write('P3', 'Market Rate', bold )
    worksheet.write('Q3', 'CO Rate / Book Rate', bold )
    worksheet.write('R3', 'Total Value Added', bold )

    '''




    j = 0
    count_record = 1
    row_record = count_record + 3
    sum = 0;
    for y in DealNumber:

        for x in usdIndex_get_DealNumbers:
            date_133US = FX133TradeData[32][x].replace(".","/");
            date_133USobj = datetime.datetime.strptime(date_133US, '%d/%m/%Y')
            periodUS = (date_133USobj-TradeData[9][approved_index[j]]).days
            if (date_133USobj.date()).weekday() >= 0 and (TradeData[9][approved_index[j]].date()).weekday() < 5 and (date_133USobj.date()).isocalendar()[1] > (TradeData[9][approved_index[j]].date()).isocalendar()[1]:

                periodUS = periodUS-2

            if y == FX133TradeData[48][x] and HqTradeData[7][j][:3] != 'DKK':
                if periodUS < 0 and (HqTradeData[7][j][:3] == 'MMK' or HqTradeData[7][j][:3] == 'ETB' or HqTradeData[7][j][:3] == 'GNF' or HqTradeData[7][j][:3] == 'JMD' or HqTradeData[7][j][:3] == 'MGA'):

                    o = 'yes'

                else:

                    if(periodUS+3) > 5:
                        the_columns = workbook.add_format({'align':'center', 'bg_color': '#ffff00', 'border': 1})
                        date_format = workbook.add_format({'num_format': 'mm/dd/yy', 'align':'center', 'bg_color': '#ffff00', 'border': 1})

                    if(periodUS+3) <= 5:
                        the_columns = workbook.add_format({'align':'center', 'border': 1})
                        date_format = workbook.add_format({'num_format': 'mm/dd/yy', 'align':'center', 'border': 1})


                    if month_dict[getmonth] == 1:
                        if TradeData[9][approved_index[j]].month == 12:

                            #--------EXCEL------------------------------

                            worksheet.write('A'+str(row_record), count_record, the_columns)
                            worksheet.write('B'+str(row_record), HqTradeData[0][j], the_columns)
                            worksheet.write('C'+str(row_record), HqTradeData[15][j].date(), date_format)
                            worksheet.write('D'+str(row_record), TradeData[9][approved_index[j]].date(), date_format)
                            worksheet.write('E'+str(row_record), str(y), the_columns)
                            worksheet.write('F'+str(row_record), "{:,.2f}".format(HqTradeData[9][j]), the_columns)
                            worksheet.write('G'+str(row_record), HqTradeData[7][j], the_columns)
                            worksheet.write('H'+str(row_record), date_133USobj.date(), date_format)
                            worksheet.write('I'+str(row_record), FX133TradeData[41][x], the_columns)
                            worksheet.write('J'+str(row_record), str(periodUS)+ ' days', the_columns)
                            worksheet.write('K'+str(row_record), str(periodUS)+' days', the_columns)
                            worksheet.write('L'+str(row_record), FX133TradeData[3][x], the_columns)

                            #dealno = HqTradeData[2][j]
                            indexed = 0

                            for check133_dealno in FX133TradeData[48]:

                                if (indexed > USDstart_index and indexed < USDstop_index) or (indexed > EURstart_index and indexed < EURstop_index):

                                    o = 'yes'

                                else:

                                    if y == check133_dealno:

                                        worksheet.write('M'+str(row_record), "{:,.2f}".format(FX133TradeData[35][indexed]), the_columns)

                                        worksheet.write('N'+str(row_record), "{:,.2f}".format(FX133TradeData[20][indexed]), the_columns)
                                        worksheet.write('O'+str(row_record), "{:,.2f}".format(FX133TradeData[13][indexed]), the_columns)
                                        worksheet.write('P'+str(row_record), "{:,.2f}".format(HqTradeData[11][j]), the_columns)
                                        worksheet.write('Q'+str(row_record), "{:,.2f}".format((FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])), the_columns)
                                        try:
                                            sum += (FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])
                                        except e:
                                            print("NaN values")
                                indexed += 1


                            '''
                            worksheet.write('M'+str(row_record), str((HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)
                            worksheet.write('N'+str(row_record), FX133TradeData[16][x], the_columns)
                            worksheet.write('O'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])), the_columns)
                            worksheet.write('P'+str(row_record), FX133TradeData[13][x], the_columns)
                            worksheet.write('Q'+str(row_record), HqTradeData[11][j], the_columns)
                            worksheet.write('R'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])-(HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)

                            '''



                            ALL_indices.append(j)
                            getPartners.append( FX133TradeData[41][x] )
                            count_record+=1
                            row_record+=1

                        else:

                            #--------EXCEL------------------------------
                            worksheet.write('A'+str(row_record), count_record, the_columns)
                            worksheet.write('B'+str(row_record), HqTradeData[0][j], the_columns)
                            worksheet.write('C'+str(row_record), HqTradeData[15][j].date(), date_format)
                            worksheet.write('D'+str(row_record), TradeData[9][approved_index[j]].date(), date_format)
                            worksheet.write('E'+str(row_record), str(y), the_columns)
                            worksheet.write('F'+str(row_record), "{:,.2f}".format(HqTradeData[9][j]), the_columns)
                            worksheet.write('G'+str(row_record), HqTradeData[7][j], the_columns)
                            worksheet.write('H'+str(row_record), date_133USobj.date(), date_format)
                            worksheet.write('I'+str(row_record), FX133TradeData[41][x], the_columns)
                            worksheet.write('J'+str(row_record), str(periodUS)+ ' days', the_columns)
                            worksheet.write('K'+str(row_record), str(periodUS+3)+' days',the_columns)
                            worksheet.write('L'+str(row_record), FX133TradeData[3][x], the_columns)

                            #dealno = HqTradeData[2][j]
                            indexed = 0

                            for check133_dealno in FX133TradeData[48]:

                                if (indexed > USDstart_index and indexed < USDstop_index) or (indexed > EURstart_index and indexed < EURstop_index):

                                    #print("Skip USD and EUR")
                                    o = 'yes'

                                else:

                                    if y == check133_dealno:

                                        worksheet.write('M'+str(row_record), "{:,.2f}".format(FX133TradeData[35][indexed]), the_columns)

                                        worksheet.write('N'+str(row_record), "{:,.2f}".format(FX133TradeData[20][indexed]), the_columns)
                                        worksheet.write('O'+str(row_record), "{:,.2f}".format(FX133TradeData[13][indexed]), the_columns)
                                        worksheet.write('P'+str(row_record), "{:,.2f}".format(HqTradeData[11][j]), the_columns)
                                        worksheet.write('Q'+str(row_record), "{:,.2f}".format((FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])), the_columns)
                                        try:
                                            sum += (FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])
                                        except e:
                                            print("NaN values")
                                indexed += 1
                            '''
                            worksheet.write('M'+str(row_record), str((HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)
                            worksheet.write('N'+str(row_record), FX133TradeData[16][x], the_columns)
                            worksheet.write('O'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])), the_columns)
                            worksheet.write('P'+str(row_record), FX133TradeData[13][x], the_columns)
                            worksheet.write('Q'+str(row_record), HqTradeData[11][j], the_columns)
                            worksheet.write('R'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])-(HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)

                            '''


                            ALL_indices.append(j)
                            getPartners.append( FX133TradeData[41][x] )
                            count_record+=1
                            row_record+=1
                    else:
                        if TradeData[9][approved_index[j]].month == (month_dict[getmonth] - 1):

                            #--------EXCEL------------------------------
                            worksheet.write('A'+str(row_record), count_record, the_columns)
                            worksheet.write('B'+str(row_record), HqTradeData[0][j], the_columns)
                            worksheet.write('C'+str(row_record), HqTradeData[15][j].date(), date_format)
                            worksheet.write('D'+str(row_record), TradeData[9][approved_index[j]].date(), date_format)
                            worksheet.write('E'+str(row_record), str(y), the_columns)
                            worksheet.write('F'+str(row_record), "{:,.2f}".format(HqTradeData[9][j]))
                            worksheet.write('G'+str(row_record), HqTradeData[7][j], the_columns)
                            worksheet.write('H'+str(row_record), date_133USobj.date(), date_format)
                            worksheet.write('I'+str(row_record), FX133TradeData[41][x], the_columns)
                            worksheet.write('J'+str(row_record), str(periodUS)+ ' days', the_columns)
                            worksheet.write('K'+str(row_record), str(periodUS)+' days', the_columns)
                            worksheet.write('L'+str(row_record), FX133TradeData[3][x], the_columns)

                            #dealno = HqTradeData[2][j]
                            indexed = 0

                            for check133_dealno in FX133TradeData[48]:

                                if (indexed > USDstart_index and indexed < USDstop_index) or (indexed > EURstart_index and indexed < EURstop_index):

                                    #print("Skip USD and EUR")
                                    o = 'yes'

                                else:

                                    if y == check133_dealno:

                                        worksheet.write('M'+str(row_record), "{:,.2f}".format(FX133TradeData[35][indexed]), the_columns)

                                        worksheet.write('N'+str(row_record), "{:,.2f}".format(FX133TradeData[20][indexed]), the_columns)
                                        worksheet.write('O'+str(row_record), "{:,.2f}".format(FX133TradeData[13][indexed]), the_columns)
                                        worksheet.write('P'+str(row_record), "{:,.2f}".format(HqTradeData[11][j]), the_columns)
                                        worksheet.write('Q'+str(row_record), "{:,.2f}".format((FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])), the_columns)
                                        try:
                                            sum += (FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])
                                        except e:
                                            print("NaN values")
                                indexed += 1
                            '''
                            worksheet.write('M'+str(row_record), str((HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)
                            worksheet.write('N'+str(row_record), FX133TradeData[16][x], the_columns)
                            worksheet.write('O'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])), the_columns)
                            worksheet.write('P'+str(row_record), FX133TradeData[13][x], the_columns)
                            worksheet.write('Q'+str(row_record), HqTradeData[11][j], the_columns)
                            worksheet.write('R'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])-(HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)

                            '''



                            ALL_indices.append(j)
                            getPartners.append( FX133TradeData[41][x] )
                            count_record+=1
                            row_record+=1

                        else:

                            #--------EXCEL------------------------------

                            worksheet.write('A'+str(row_record), count_record, the_columns)
                            worksheet.write('B'+str(row_record), HqTradeData[0][j], the_columns)
                            worksheet.write('C'+str(row_record), HqTradeData[15][j].date(), date_format)
                            worksheet.write('D'+str(row_record), TradeData[9][approved_index[j]].date(), date_format)
                            worksheet.write('E'+str(row_record), str(y), the_columns)
                            worksheet.write('F'+str(row_record), "{:,.2f}".format(HqTradeData[9][j]), the_columns)
                            worksheet.write('G'+str(row_record), HqTradeData[7][j], the_columns)
                            worksheet.write('H'+str(row_record), date_133USobj.date(), date_format)
                            worksheet.write('I'+str(row_record), FX133TradeData[41][x], the_columns)
                            worksheet.write('J'+str(row_record), str(periodUS)+ ' days', the_columns)
                            worksheet.write('K'+str(row_record), str(periodUS+3)+' days', the_columns)
                            worksheet.write('L'+str(row_record), FX133TradeData[3][x], the_columns)

                            #dealno = HqTradeData[2][j]
                            indexed = 0

                            for check133_dealno in FX133TradeData[48]:

                                if (indexed > USDstart_index and indexed < USDstop_index) or (indexed > EURstart_index and indexed < EURstop_index):

                                    #print("Skip USD and EUR")
                                    o = 'yes'

                                else:

                                    if y == check133_dealno:

                                        worksheet.write('M'+str(row_record), "{:,.2f}".format(FX133TradeData[35][indexed]), the_columns)

                                        worksheet.write('N'+str(row_record), "{:,.2f}".format(FX133TradeData[20][indexed]), the_columns)
                                        worksheet.write('O'+str(row_record), "{:,.2f}".format(FX133TradeData[13][indexed]), the_columns)
                                        worksheet.write('P'+str(row_record), "{:,.2f}".format(HqTradeData[11][j]), the_columns)
                                        worksheet.write('Q'+str(row_record), "{:,.2f}".format((FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])), the_columns)
                                        try:
                                            sum += (FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])
                                        except e:
                                            print("NaN values")
                                indexed += 1
                            '''
                            worksheet.write('M'+str(row_record), str((HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)
                            worksheet.write('N'+str(row_record), FX133TradeData[16][x], the_columns)
                            worksheet.write('O'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])), the_columns)
                            worksheet.write('P'+str(row_record), FX133TradeData[13][x], the_columns)
                            worksheet.write('Q'+str(row_record), HqTradeData[11][j], the_columns)
                            worksheet.write('R'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])-(HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)

                            '''

                            ALL_indices.append(j)
                            getPartners.append( FX133TradeData[41][x] )
                            count_record+=1
                            row_record+=1

        for x in EURIndex_get_DealNumbers:
            date_133EU = FX133TradeData[32][x].replace(".","/");
            date_133EUobj = datetime.datetime.strptime(date_133EU, '%d/%m/%Y')
            periodEU = (date_133EUobj-TradeData[9][approved_index[j]]).days
            if (date_133EUobj.date()).weekday() >= 0 and (TradeData[9][approved_index[j]].date()).weekday() < 5 and (date_133EUobj.date()).isocalendar()[1] > (TradeData[9][approved_index[j]].date()).isocalendar()[1]:
                periodEU = periodEU-2
            if y == FX133TradeData[48][x] and HqTradeData[7][j][:3] != 'DKK':

                if periodEU < 0 and (HqTradeData[7][j][:3] == 'MMK' or HqTradeData[7][j][:3] == 'ETB' or HqTradeData[7][j][:3] == 'GNF' or HqTradeData[7][j][:3] == 'JMD' or HqTradeData[7][j][:3] == 'MGA'):

                    o = 'yes'

                else:

                    if(periodEU+3) > 5:
                        the_columns = workbook.add_format({'align':'center', 'bg_color': '#ffff00', 'border': 1})
                        date_format = workbook.add_format({'num_format': 'mm/dd/yy', 'align':'center', 'bg_color': '#ffff00', 'border': 1})

                    if(periodEU+3) <= 5:
                        the_columns = workbook.add_format({'align':'center', 'border': 1})
                        date_format = workbook.add_format({'num_format': 'mm/dd/yy', 'align':'center', 'border': 1})

                    if month_dict[getmonth] == 1:

                        if TradeData[9][approved_index[j]].month == 12:

                            #--------EXCEL------------------------------
                            worksheet.write('A'+str(row_record), count_record, the_columns)
                            worksheet.write('B'+str(row_record), HqTradeData[0][j], the_columns)
                            worksheet.write('C'+str(row_record), HqTradeData[15][j].date(), date_format)
                            worksheet.write('D'+str(row_record), TradeData[9][approved_index[j]].date(), date_format)
                            worksheet.write('E'+str(row_record), str(y), the_columns)
                            worksheet.write('F'+str(row_record), "{:,.2f}".format(HqTradeData[9][j]), the_columns)
                            worksheet.write('G'+str(row_record), HqTradeData[7][j], the_columns)
                            worksheet.write('H'+str(row_record), date_133EUobj.date(), date_format)
                            worksheet.write('I'+str(row_record), FX133TradeData[41][x], the_columns)
                            worksheet.write('J'+str(row_record), str(periodEU)+ ' days', the_columns)
                            worksheet.write('K'+str(row_record), str(periodEU)+' days', the_columns)
                            worksheet.write('L'+str(row_record), FX133TradeData[3][x], the_columns )

                            #dealno = HqTradeData[2][j]
                            indexed = 0

                            for check133_dealno in FX133TradeData[48]:

                                if (indexed > USDstart_index and indexed < USDstop_index) or (indexed > EURstart_index and indexed < EURstop_index):

                                    #print("Skip USD and EUR")
                                    o = 'yes'

                                else:

                                    if y == check133_dealno:

                                        worksheet.write('M'+str(row_record), "{:,.2f}".format(FX133TradeData[35][indexed]), the_columns)

                                        worksheet.write('N'+str(row_record), "{:,.2f}".format(FX133TradeData[20][indexed]), the_columns)
                                        worksheet.write('O'+str(row_record), "{:,.2f}".format(FX133TradeData[13][indexed]), the_columns)
                                        worksheet.write('P'+str(row_record), "{:,.2f}".format(HqTradeData[11][j]), the_columns)
                                        worksheet.write('Q'+str(row_record), "{:,.2f}".format((FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])), the_columns)
                                        try:
                                            sum += (FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])
                                        except e:
                                            print("NaN values")
                                indexed += 1

                            '''
                            worksheet.write('M'+str(row_record), str((HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)
                            worksheet.write('N'+str(row_record), FX133TradeData[16][x], the_columns)
                            worksheet.write('O'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])), the_columns)
                            worksheet.write('P'+str(row_record), FX133TradeData[13][x], the_columns)
                            worksheet.write('Q'+str(row_record), HqTradeData[11][j], the_columns)
                            worksheet.write('R'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])-(HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)

                            '''


                            ALL_indices.append(j)
                            getPartners.append( FX133TradeData[41][x] )
                            count_record+=1
                            row_record+=1
                        else:

                            #--------EXCEL------------------------------
                            worksheet.write('A'+str(row_record), count_record, the_columns)
                            worksheet.write('B'+str(row_record), HqTradeData[0][j], the_columns)
                            worksheet.write('C'+str(row_record), HqTradeData[15][j].date(), date_format)
                            worksheet.write('D'+str(row_record), TradeData[9][approved_index[j]].date(), date_format)
                            worksheet.write('E'+str(row_record), str(y), the_columns)
                            worksheet.write('F'+str(row_record), "{:,.2f}".format(HqTradeData[9][j]), the_columns)
                            worksheet.write('G'+str(row_record), HqTradeData[7][j], the_columns)
                            worksheet.write('H'+str(row_record), date_133EUobj.date(), date_format)
                            worksheet.write('I'+str(row_record), FX133TradeData[41][x], the_columns)
                            worksheet.write('J'+str(row_record), str(periodEU)+ ' days', the_columns)
                            worksheet.write('K'+str(row_record), str(periodEU+3)+' days', the_columns)
                            worksheet.write('L'+str(row_record), FX133TradeData[3][x], the_columns)

                            #dealno = HqTradeData[2][j]
                            indexed = 0

                            for check133_dealno in FX133TradeData[48]:

                                if (indexed > USDstart_index and indexed < USDstop_index) or (indexed > EURstart_index and indexed < EURstop_index):

                                    #print("Skip USD and EUR")
                                    o = 'yes'

                                else:

                                    if y == check133_dealno:

                                        worksheet.write('M'+str(row_record), "{:,.2f}".format(FX133TradeData[35][indexed]), the_columns)

                                        worksheet.write('N'+str(row_record), "{:,.2f}".format(FX133TradeData[20][indexed]), the_columns)
                                        worksheet.write('O'+str(row_record), "{:,.2f}".format(FX133TradeData[13][indexed]), the_columns)
                                        worksheet.write('P'+str(row_record), "{:,.2f}".format(HqTradeData[11][j]), the_columns)
                                        worksheet.write('Q'+str(row_record), "{:,.2f}".format((FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])), the_columns)
                                        try:
                                            sum += (FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])
                                        except e:
                                            print("NaN values")
                                indexed += 1
                            '''
                            worksheet.write('M'+str(row_record), str((HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)
                            worksheet.write('N'+str(row_record), FX133TradeData[16][x], the_columns)
                            worksheet.write('O'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])), the_columns)
                            worksheet.write('P'+str(row_record), FX133TradeData[13][x], the_columns)
                            worksheet.write('Q'+str(row_record), HqTradeData[11][j], the_columns)
                            worksheet.write('R'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])-(HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)

                            '''
                               #trade_writer.writerow([count_record, HqTradeData[0][j],HqTradeData[15][j].date(),TradeData[9][approved_index[j]].date(),str(y),"{:,.2f}".format(HqTradeData[9][j]),HqTradeData[7][j],date_133EUobj.date(),FX133TradeData[41][x],str(periodEU)+' days',str(periodEU+3)+' days',FX133TradeData[3][x] ])
                            ALL_indices.append(j)
                            getPartners.append( FX133TradeData[41][x] )
                            count_record+=1
                            row_record+=1
                    else:
                        if TradeData[9][approved_index[j]].month == (month_dict[getmonth] - 1):
                            #--------EXCEL------------------------------
                            worksheet.write('A'+str(row_record), count_record, the_columns)
                            worksheet.write('B'+str(row_record), HqTradeData[0][j], the_columns)
                            worksheet.write('C'+str(row_record), HqTradeData[15][j].date(), date_format)
                            worksheet.write('D'+str(row_record), TradeData[9][approved_index[j]].date(), date_format)
                            worksheet.write('E'+str(row_record), str(y), the_columns)
                            worksheet.write('F'+str(row_record), "{:,.2f}".format(HqTradeData[9][j]))
                            worksheet.write('G'+str(row_record), HqTradeData[7][j], the_columns)
                            worksheet.write('H'+str(row_record), date_133EUobj.date(), date_format)
                            worksheet.write('I'+str(row_record), FX133TradeData[41][x], the_columns)
                            worksheet.write('J'+str(row_record), str(periodEU)+ ' days', the_columns)
                            worksheet.write('K'+str(row_record), str(periodEU)+' days', the_columns)
                            worksheet.write('L'+str(row_record), FX133TradeData[3][x], the_columns)

                            #dealno = HqTradeData[2][j]
                            indexed = 0

                            for check133_dealno in FX133TradeData[48]:

                                if (indexed > USDstart_index and indexed < USDstop_index) or (indexed > EURstart_index and indexed < EURstop_index):

                                    #print("Skip USD and EUR")
                                    o = 'yes'

                                else:

                                    if y == check133_dealno:

                                        worksheet.write('M'+str(row_record), "{:,.2f}".format(FX133TradeData[35][indexed]), the_columns)

                                        worksheet.write('N'+str(row_record), "{:,.2f}".format(FX133TradeData[20][indexed]), the_columns)
                                        worksheet.write('O'+str(row_record), "{:,.2f}".format(FX133TradeData[13][indexed]), the_columns)
                                        worksheet.write('P'+str(row_record), "{:,.2f}".format(HqTradeData[11][j]), the_columns)
                                        worksheet.write('Q'+str(row_record), "{:,.2f}".format((FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])), the_columns)
                                        try:
                                            sum += (FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])
                                        except e:
                                            print("NaN values")
                                indexed += 1

                            '''
                            worksheet.write('M'+str(row_record), str((HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)
                            worksheet.write('N'+str(row_record), FX133TradeData[16][x], the_columns)
                            worksheet.write('O'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])), the_columns)
                            worksheet.write('P'+str(row_record), FX133TradeData[13][x], the_columns)
                            worksheet.write('Q'+str(row_record), HqTradeData[11][j], the_columns)
                            worksheet.write('R'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])-(HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)

                            '''
                            #trade_writer.writerow([count_record, HqTradeData[0][j],HqTradeData[15][j].date(),TradeData[9][approved_index[j]].date(),str(y),"{:,.2f}".format(HqTradeData[9][j]),HqTradeData[7][j],date_133EUobj.date(),FX133TradeData[41][x],str(periodEU)+' days',str(periodEU)+' days',FX133TradeData[3][x] ])
                            ALL_indices.append(j)
                            getPartners.append( FX133TradeData[41][x] )
                            count_record+=1
                            row_record+=1
                        else:
                            #--------EXCEL------------------------------
                            worksheet.write('A'+str(row_record), count_record, the_columns)
                            worksheet.write('B'+str(row_record), HqTradeData[0][j], the_columns)
                            worksheet.write('C'+str(row_record), HqTradeData[15][j].date(), date_format)
                            worksheet.write('D'+str(row_record), TradeData[9][approved_index[j]].date(), date_format)
                            worksheet.write('E'+str(row_record), str(y), the_columns)
                            worksheet.write('F'+str(row_record), "{:,.2f}".format(HqTradeData[9][j]), the_columns)
                            worksheet.write('G'+str(row_record), HqTradeData[7][j], the_columns)
                            worksheet.write('H'+str(row_record), date_133EUobj.date(), date_format)
                            worksheet.write('I'+str(row_record), FX133TradeData[41][x], the_columns)
                            worksheet.write('J'+str(row_record), str(periodEU)+ ' days', the_columns)
                            worksheet.write('K'+str(row_record), str(periodEU+3)+' days', the_columns)
                            worksheet.write('L'+str(row_record), FX133TradeData[3][x], the_columns)

                            #dealno = HqTradeData[2][j]
                            indexed = 0

                            for check133_dealno in FX133TradeData[48]:

                                if (indexed > USDstart_index and indexed < USDstop_index) or (indexed > EURstart_index and indexed < EURstop_index):

                                    #print("Skip USD and EUR")
                                    o = 'yes'

                                else:

                                    if y == check133_dealno:

                                        worksheet.write('M'+str(row_record), "{:,.2f}".format(FX133TradeData[35][indexed]), the_columns)

                                        worksheet.write('N'+str(row_record), "{:,.2f}".format(FX133TradeData[20][indexed]), the_columns)
                                        worksheet.write('O'+str(row_record), "{:,.2f}".format(FX133TradeData[13][indexed]), the_columns)
                                        worksheet.write('P'+str(row_record), "{:,.2f}".format(HqTradeData[11][j]), the_columns)
                                        worksheet.write('Q'+str(row_record), "{:,.2f}".format((FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])), the_columns)
                                        try:
                                            sum += (FX133TradeData[20][indexed])-(FX133TradeData[13][indexed])
                                        except e:
                                            print("NaN values")


                                indexed += 1


                            '''
                            worksheet.write('M'+str(row_record), str((HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)
                            worksheet.write('N'+str(row_record), FX133TradeData[16][x], the_columns)
                            worksheet.write('O'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])), the_columns)
                            worksheet.write('P'+str(row_record), FX133TradeData[13][x], the_columns)
                            worksheet.write('Q'+str(row_record), HqTradeData[11][j], the_columns)
                            worksheet.write('R'+str(row_record), str((HqTradeData[9][j]/HqTradeData[11][j])-(HqTradeData[9][j]/FX133TradeData[13][x])), the_columns)

                            '''

                            #trade_writer.writerow([count_record, HqTradeData[0][j],HqTradeData[15][j].date(),TradeData[9][approved_index[j]].date(),str(y),"{:,.2f}".format(HqTradeData[9][j]),HqTradeData[7][j],date_133EUobj.date(),FX133TradeData[41][x],str(periodEU)+' days',str(periodEU+3)+' days',FX133TradeData[3][x] ])
                            ALL_indices.append(j)
                            getPartners.append( FX133TradeData[41][x] )
                            count_record+=1
                            row_record+=1


        j+=1
    worksheet.write('P'+str(row_record), "TOTAL", bold)
    worksheet.write('Q'+str(row_record), "{:,.2f}".format(sum), bold)
    worksheet.merge_range('O'+str(row_record+1)+':Q'+str(row_record+1), "Compiled by: Louisa Tinga - Treasury Unit")

    for delete in files:

        os.remove('files/'+delete);

    missing_indices = []
    for y in range( 0, (ALL_indices[-1] + 1) ):
        if y not in ALL_indices:
            missing_indices.append(y)
    print('\n')
    print('Records missing equals: ',len(missing_indices))
    print ('See missing records below: ')
    for y in missing_indices:
        print('Missing index: ',y,'; Deal Number: ',HqTradeData[2][y], '; Currency: ',HqTradeData[7][y],'; Deal Amount: ', "{:,}".format( HqTradeData[9][y] ), '; Creation date: ',HqTradeData[15][y], '; Value date CO: ',HqTradeData[8][y])
    print('\n')

    x = getPartners
    dict = {}

    for p in getPartners:
        count = 0
        for q in x:
            if p == q:
                count+=1
        dict[p] = count
    total_transactions = 0
    for x in dict:
        print(x, dict[x])
        total_transactions = total_transactions+dict[x]
    print('\n', 'The total number of transactions equals:',total_transactions)
    workbook.close()


    '''
    for h in ALL_indices:
        dealno = HqTradeData[2][h]
        index = 0
        count = 0
        for check133_dealno in FX133TradeData[48]:

            if dealno == check133_dealno and count < 1:
                print('Deal Number: ', dealno, 'FX133 index: ', index, 'Market rate: ', FX133TradeData[35][index], 'Base Curr Equiv[CO Rate]: ', FX133TradeData[20][index], 'Base Curr Equiv[Market Rate]: ', FX133TradeData[13][index], 'Value Add: ', (FX133TradeData[20][index] - FX133TradeData[13][index]) )
                count += 1
            index += 1

    '''





#=======================

import pandas as pd
import json

class preproccessing_ticker_symbol():

    def get_ticker_symbol():
        symbol_df = pd.read_csv('../data/companies/wikidata_ticker_symbol_data.csv')
        list_df_1 = pd.read_csv('../data/companies/wikilist_1.csv', encoding='latin-1')
        list_df_2 = pd.read_csv('../data/companies/wikilist_2.csv', encoding='latin-1')

        len(symbol_df["tickerSymbol"].unique())
        # check which companies are missing in the wikidata_ticker_symbol_data.csv 
        result_list = []
        result_list.extend(symbol_df["tickerSymbol"].to_list())

        list_of_ticker_symbols_1 = list_df_1["Symbol"].unique()


        missing_ticker_symbols = []
        for symbol in list_of_ticker_symbols_1:
            if symbol not in symbol_df["tickerSymbol"].unique():
                missing_ticker_symbols.append({"symbol":symbol, "list":"first"})
                result_list.append(symbol)

        list_of_ticker_symbols_2 = list_df_2["Removed"].unique()
        for symbol in list_of_ticker_symbols_2:
            if symbol not in symbol_df["tickerSymbol"].unique():
                missing_ticker_symbols.append({"symbol":symbol, "list":"second"})
                result_list.append(symbol)

        print(missing_ticker_symbols)
        
        
        print(len(set(result_list)))

        return result_list
    

class preproccessing_alphavantage_data():
    def __init__(self) -> None:
        data = ""
        with open('../data/stock_infos/result.json') as json_file:
            data = json_file.read()
        self.data_as_json = json.loads(data)

    def normalize_data(self):
        # normalize data
        normalized_json_df = pd.json_normalize(self.data_as_json)
        normalized_json_df = normalized_json_df.drop_duplicates("Meta Data.2. Symbol")
        normalized_json_df = normalized_json_df.dropna(axis=0,subset=["Meta Data.2. Symbol"])
        normalized_json_df = normalized_json_df.set_index("Meta Data.2. Symbol")

        transposed_df =  normalized_json_df.transpose()
        transposed_df = transposed_df.reset_index()

        transposed_df["index_extracted"] = transposed_df["index"].replace({r".*(\d\d\d\d-\d\d-\d\d)(.*)": r"\1 \2"}, regex=True)
        transposed_df[["date", "random_counter", "information"]] = transposed_df["index_extracted"].str.split(".", expand=True)
        transposed_df["date"] = pd.to_datetime(transposed_df["date"], errors="coerce")
        transposed_df.dropna(subset=['date'], inplace=True)

        # set every column to numeric except date, random_counter and information and index_extracted
        for x in transposed_df.columns:
            if(x != "date" and x != "random_counter" and x != "information" and x != "index_extracted" and x != "index"):
                transposed_df[x] = transposed_df[x].astype(float)

        return transposed_df




class preproccessing_fmp_data():
    
    def __init__(self) -> None:
        self.raw_data = []
        self.raw_data_stock = []
        with open('../data/stock_infos/raw_data_fmp.json', "r") as json_file:
            self.raw_data = json.load(json_file)

        with open('../data/stock_infos/raw_data_fmp_stock_value.json', "r") as json_file:
            self.raw_data_stock = json.load(json_file)

    def normalize_stock_data(self):

        # same as above but for stock value

        self.raw_data_stock[1].keys()



        pd.json_normalize(self.raw_data_stock[0]["data"]).keys()

        df_stock = pd.DataFrame(pd.json_normalize(self.raw_data_stock[0]["data"]))
        df_stock["date"] = pd.to_datetime(df_stock["date"]).dt.to_period('M')
        print(df_stock.columns)
        df_stock
        from datetime import datetime, timedelta

        # Starting date (January 1, 1970)
        start_date = datetime(1970, 1, 1)

        # Number of months to generate
        num_months = (datetime.now() - start_date).days // 30

        # Generate datetime objects for each month
        months = [start_date + timedelta(days=30 * i) for i in range(num_months)]


        result_df = pd.DataFrame()


        result_df["date"] = pd.to_datetime(months).to_period('M')



        for i, x in enumerate(self.raw_data_stock):
            
            try:
            # unpivot json
                df = pd.json_normalize(x['data'])
            except:
                # print(x)
                # input()
                continue
            
            if(df.empty):
                continue
            # show me df if column date does not exist
            if("date" not in df.columns):
                
                continue

            
            df['date'] = pd.to_datetime(df['date'], errors='coerce').dropna()
            # df['date'] = pd.to_datetime(df['date']).dt.to_period('M')

            df['date'] = df['date'].dt.to_period('M')
                
            df_melted = df.melt(id_vars=['date'], value_vars=['date', 'open', 'low', 'high', 'close', 'volume'])
            print(x['symbol'])
            # rename value column to json_response_2['symbol']
            # df_melted = df_melted.rename(columns={"value": x['symbol']})
            # join result df with df_melted on date
            df_melted["symbol"] = x["symbol"]



            if(i == 0):
                result_df = df_melted
                continue
            
            result_df = pd.concat([result_df, df_melted])

            # result_df = result_df.merge(df_melted, how='left', on='date')
            
            


        # result_df[(result_df["variable"] == "close") & (result_df["symbol"] == "PFE") ]
        # result_df.to_csv("./data/stock_infos/stock_values_per_symbol.csv", index=False)

        return result_df

















        pass

    def normalize_dividenden_data(self):

        result_df = pd.DataFrame()

        from datetime import datetime, timedelta

        # Starting date (January 1, 1970)
        start_date = datetime(1970, 1, 1)

        # Number of months to generate
        num_months = (datetime.now() - start_date).days // 30

        # Generate datetime objects for each month
        months = [start_date + timedelta(days=30 * i) for i in range(num_months)]


        result_df["date"] = pd.to_datetime(months).to_period('M')



        for i, x in enumerate(self.raw_data):
            
            try:

            # unpivot json
                df = pd.json_normalize(x['historical'])
            except:
                # shows which company ticker is not working
                # print(x)
                continue
            
            if(df.empty):
                continue
            

            
            df['orignal_date'] = pd.to_datetime(df['date'])
            # df['date'] = pd.to_datetime(df['date']).dt.to_period('M')

            df['date'] = df['orignal_date'].dt.to_period('M')
                
            df_melted = df.melt(id_vars=['date'], value_vars=['adjDividend', 'dividend', "recordDate", "paymentDate", "declarationDate"])
            # print(x['symbol'])
            # rename value column to json_response_2['symbol']
            # df_melted = df_melted.rename(columns={"value": x['symbol']})
            # join result df with df_melted on date
            df_melted["symbol"] = x["symbol"]



            if(i == 0):
                result_df = df_melted
                continue
            
            result_df = pd.concat([result_df, df_melted])

            # result_df = result_df.merge(df_melted, how='left', on='date')
            
            


        # result_df[(result_df["variable"] == "adjDividend") & (result_df["symbol"] == "MSFT") ]
        # result_df.to_csv("../data/stock_infos/dividend_values_per_symbol.csv", index=False)
        print(result_df.columns)
        return result_df
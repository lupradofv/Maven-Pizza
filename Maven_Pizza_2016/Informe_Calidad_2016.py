import pandas as pd

files = ['order_details.csv','orders.csv']
for csv in files:
    data = pd.read_csv(csv,sep=';')
    data_types = pd.DataFrame(data.dtypes, columns=['Data Type'])
    data_count = pd.DataFrame(data.count(), columns=['Data Count'])
    null = pd.DataFrame(data.isnull().sum(),columns=['Null Count'])
    null_percentage = pd.DataFrame((data.isnull().sum()/data.count())*100,columns=['Null Percentage (%)'])
    nan = pd.DataFrame(data.isna().sum(),columns=['NaN Count'])
    nan_percentage = pd.DataFrame((data.isna().sum()/data.count())*100,columns=['NaN Percentage (%)'])
    unique_values = pd.DataFrame(columns=['Unique Values'])
    for r in data.columns.values:
        unique_values.loc[r] = [data[r].nunique()]
    
    dq_report = data_types.join(data_count).join(null).join(null_percentage).join(nan).join(nan_percentage).join(unique_values)
    print()
    print(dq_report)
    dq_report.to_csv(csv[:-4]+'_informe.csv')
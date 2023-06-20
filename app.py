import pandas as pd
from sqlalchemy import create_engine
import pymssql
import streamlit as st
import streamlit_nested_layout
import datetime

st.set_page_config(layout="wide")

database_p = "20.169.221.14:1433/Bayview_Automation"
userandpass = '//sa:3004222950A.b@'
engine = create_engine('mssql+pymssql:'+userandpass+database_p)


conn = pymssql.connect("20.169.221.14:1433","sa","3004222950A.b","Bayview_Automation")
cursor = conn.cursor()




data_table_query = """  SELECT * FROM [STG_MR].[MERGED] WHERE [REPORT DATE] = (SELECT MAX([REPORT DATE]) FROM [STG_MR].MERGED) """
df_table = pd.read_sql(con= engine, sql= data_table_query)
df_table["Pool Issue Date"] = pd.to_datetime(df_table["Pool Issue Date"], format="%m/%d/%Y").dt.date
df_table["OPB"] = pd.to_numeric(df_table["OPB"])

def title_centered_h3(str_):
    title = st.markdown("""<h3 style='text-align: center'>""" + str(str_) +"""</h3>""",unsafe_allow_html =True)
    return title
def title_centered_h4(str_):
    title = st.markdown("""<h4 style='text-align: center'>""" + str(str_) +"""</h4>""",unsafe_allow_html =True)
    return title
def title_centered_h1(str_):
    title = st.markdown("""<h1 style='text-align: center'>""" + str(str_) +"""</h1>""",unsafe_allow_html =True)
    return title
def space():
    return st.markdown("<br>", unsafe_allow_html=True)
def line():
    return st.markdown("<hr>",unsafe_allow_html=True)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


sql1 = """ SELECT [Unique Loan Id] FROM [STG_MR].[MERGED] """
sql1_df = pd.read_sql(con=engine,sql=sql1)
list_loans = sql1_df['Unique Loan Id'].to_list()


latest_update_query =  "SELECT MAX([REPORT DATE]) AS MX FROM [STG_MR].[MERGED]"
SQ_DF= pd.read_sql(con= engine,sql=latest_update_query)
max_date = SQ_DF["MX"].to_list()[0]

title_centered_h1("Ginnie Mae project")
space()
_0, _1 = st.columns([10,1])
with _1:
    st.markdown(f"Last report : <br> {max_date}",unsafe_allow_html=True)
cont_1 = st.container()
with cont_1:

    col1,col2 = st.columns([1,4])

    with col1:


        st.image("Ginnie_Mae_logo.png",use_column_width=True)

        loan_selector = st.selectbox('Select Loan Id',list_loans)
        sql2  = """ SELECT [Action],[Notes 3rd Party],[Notes Internal] FROM [STG_MR].[MERGED] WHERE [Unique Loan Id] = """ + str(loan_selector)
        sql2_df = pd.read_sql(con=engine,sql = sql2)

        action = sql2_df.iloc[0,0]
        Notes_3rd = sql2_df.iloc[0,1]
        notes_internal = sql2_df.iloc[0,2]
        
        title_centered_h4('Action')
        actions_ =st.text_input(label='action',label_visibility ='hidden')
        title_centered_h4('Notes 3rd Party')
        nostes3rd_ = st.text_input(label='Notes 3rd Party',label_visibility ='hidden')
        title_centered_h4('Notes Internal')
        notes_internal_ = st.text_input(label='Notes Internal',label_visibility ='hidden')


        d1,d2,d3,d4,d5,d6,d7 =st.columns(7)
        with d4:
            if st.button('Upload Notes'):
                cursor.execute("""
                UPDATE [STG_MR].[MERGED]  
                SET 
                    [Action] = """ + """'""" + str(actions_) + """'""" + ""","""+ """ [Notes Internal] = '""" +  str(notes_internal_) + """'""" + """,[Notes 3rd Party] = """  + """'""" + str(nostes3rd_) + """'""" + """ WHERE [Unique Loan Id] = """ +str(loan_selector))
                conn.commit()
                conn.close()
                st.write("Updated")
                print("Done")

    with col2: 

        df_table = df_table[
                [
                    "Unique Loan Id",
                    "Action",
                    "Loan Type",
                    "Next Due Date",
                    "Mas Aged/Other Reporting",
                    "Loan Purpose",
                    "Notes 3rd Party",
                    "Notes Internal",
                    "Loan Closing Date",
                    "Release Date",
                    "Seller",
                    "Seller ID",
                    "Sub",
                    "Borrower",
                    "State",
                    "Insurance Status",
                    "Pool Id",
                    "Case Number",
                    "Issuer Loan Id",
                    "Guaranty_Percent",
                    "Guaranty_Amount",
                    "Loan Amount",
                    "RHS Borrower Reported",
                    "Match Code",
                    "Matching Date",
                    "OPB",
                    "Agency Maturity Date",
                    "Loan Maturity Date",
                    "Agency Interest Rate",
                    "Loan Interest Rate",
                    "Agency ZIP code",
                    "Pool Issue Date",
                    "Loan ZIP Code"
                    ]
                ]

        #Define Filters



        cont_filters = st.container()
        
        with cont_filters:
            d1,d2 = st.columns([4,1])
            
            with st.container():
        
                with d1:
                    dropdown_report_type = st.multiselect(
                        label = "MAS Aged / Other Reporting",
                        options = df_table["Mas Aged/Other Reporting"].drop_duplicates(),
                        default= [x for x in df_table["Mas Aged/Other Reporting"].drop_duplicates().to_list() if "Mas" in x  ] )
                                    
                    dropdown_match_code = st.multiselect(
                        label = "Match Code",
                        options = df_table["Match Code"].drop_duplicates(),
                        default =[])
                    
                    dropdown_subservicer = st.multiselect(
                        label = "Subservicer",
                        options = df_table["Sub"].drop_duplicates(),
                        default= []  )

            with d2:
                
                space()
                if dropdown_report_type != []:
                    _df_1 = df_table[df_table["Mas Aged/Other Reporting"].isin(dropdown_report_type)]
                else:
                    _df_1 = df_table.copy()

                if dropdown_match_code != []:
                    _df_2 = _df_1[_df_1["Match Code"].isin(dropdown_match_code)]
                else:
                    _df_2 = _df_1.copy()

                if dropdown_subservicer !=[]:
                    _df_3 = _df_2[_df_2["Sub"].isin(dropdown_subservicer)]
                else:
                    _df_3 = _df_2.copy()

                st.info(f"\n Number of Loans :\n\n\n\n\n\n\n\n\n  {len(_df_3)}")
                opb_sum= _df_3["OPB"].sum()
                st.info(f"Total OPB : \n\n\n\n\n\n\n\n\n $ {opb_sum:,.2f}")



        def highlight_cells(row):
            date_str = row['Pool Issue Date']
            if pd.isnull(date_str):  # Handle missing or invalid dates
                return [''] * len(row)

            Pool_Issue_Date = pd.to_datetime(date_str).date()
            today = datetime.datetime.now().date()
            difference = today - Pool_Issue_Date

            if difference.days > 90:
                return ['background-color: red ; color: white'] * len(row)
            elif difference.days > 60:
                return ['background-color: orange ; color: white'] * len(row) 
            else:
                return [''] * len(row)

        # Apply the function to the desired subset of the dataframe
        styled_df = _df_3.style.apply(highlight_cells, axis=1, subset=pd.IndexSlice[:, ['Unique Loan Id', 'Pool Issue Date']])
       
        
        st.dataframe(styled_df,use_container_width=True, height=600 )



line()



s = """SELECT [Unique Loan Id],Action,[Notes 3rd Party],[Notes Internal],RESOLUTION,[REPORT DATE] FROM STG_MR.MERGED
WHERE Action <> '                                                                                                                                                           '
"""
s_df= pd.read_sql(con= engine,sql= s)


comment_loand_list = s_df["Unique Loan Id"].drop_duplicates()

container_second = st.container()
with container_second:

    comments1, comments2 = st.columns([1,3])
        
    with  comments1:
        comment_loans_= st.multiselect("Unique Loan Id",options = comment_loand_list,default = comment_loand_list.sample(2))
    
    with comments2:
        __sdf = s_df[s_df["Unique Loan Id"].isin(comment_loans_)]
        st.dataframe(__sdf)










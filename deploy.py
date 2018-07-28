from flask import Flask, render_template, request, Markup
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go
import pandas as pd
import numpy as np

all_vote_result_df={}
dist_const_df_total=None


#for BJP
all_bjp={}
'''
{
    'Haryana':
    {
        '2009':dframe,
        '2014':dframe,
        '2011':dframe,
    
    },
    'Assam':
    {
        '2009':dframe,
        '2014':dframe,
        '2011':dframe
    
    }

    


}
'''
'''
all_bjp
{
    "2014":dframe
    "2009":dframe
    "2004":dframe
    
}
'''

def prepare_dataset(states,years):
    global all_vote_result_df
    for state in states:
        all_vote_result_df[state]={}
        for year in years:
            df = pd.read_excel(state+".xlsx",sheet_name=year)
            # print(state,year)
            all_vote_result_df[state][year]=df


    global dist_const_df_total
    dist_const_df_total = pd.read_excel("District-Constituency.xlsx")


    #for BJP viewing
    for year in years:
        df = pd.read_excel("AllBJP.xlsx",sheet_name=year)
        all_bjp[year]=df






def main():
    print("At main, just once")
    
    #get unique states
    muslim_pop_df=pd.read_excel("District-Constituency.xlsx")
    states=muslim_pop_df.State.unique()


    prepare_dataset(states,['2014','2009','2004'])
    print("prepared data")
    #prepare dataset here?

app = Flask(__name__)

app.config["DEBUG"]=True



def give_graph_table_div(df):

    df=df.sort_values(by=['Count Of Votes'],ascending=False)
        
    winner_votes=int(df.iloc[0]["Count Of Votes"])
    state=str(df.iloc[0]["State"])
    constituency=str(df.iloc[0]["Constituency"])

    num_votes=df["Count Of Votes"].tolist()
    parties=df["Party"].tolist()
    colors=[]
    colors = ['rgba(104,204,204,1)']*len(parties)
    colors[0]='rgba(221,104,94,1)'

    data = [go.Bar(
        x=parties,
        y=num_votes,
        marker=dict(
        color=colors),
        )]
    layout = go.Layout(
        title=state+' '+constituency+' 2014',
    )

    fig = go.Figure(data=data, layout=layout)

    #to create a div for the graph
    graph_div=plot(fig,output_type='div')

    margin=num_votes[0]-num_votes[1]
    # print("BJP won by ",margin," votes")

    #here we make the first table

    table_div="<div><table><tr>"
    for party in parties:
        table_div=table_div+"<th>"+str(party)+"<th>"
    table_div=table_div+"</tr><tr>"
    for vote in num_votes:
        table_div=table_div+"<td>"+str(vote)+"<td>"
    table_div=table_div+"</tr></table></div>"

    table_div=table_div+"<div>"+"BJP wins by "+str(margin)+"votes"+"</div>"

    mix_div=graph_div+table_div







    #pitting top two against winner
    mod_parties=[]
    mod_parties.append(parties[0])
    mod_parties.append(parties[1]+" & "+parties[2])
    mod_num_votes=[]
    mod_num_votes.append(num_votes[0])
    mod_num_votes.append(num_votes[1]+num_votes[2])
    colors = ['rgba(104,204,204,1)']*len(mod_parties)
    colors[0]='rgba(221,104,94,1)'


    data = [go.Bar(
        x=mod_parties,
        y=mod_num_votes,
    marker=dict(
        color=colors),

    )]
    layout = go.Layout(
    title=state+' '+constituency+' 2014',
    )

    fig = go.Figure(data=data, layout=layout)
    #to create a div for the graph
    graph_div=plot(fig,output_type='div')
    
    table_div="<div><table><tr>"
    for party in mod_parties:
        table_div=table_div+"<th>"+str(party)+"<th>"
    table_div=table_div+"</tr><tr>"
    for vote in mod_num_votes:
        table_div=table_div+"<td>"+str(vote)+"<td>"
    table_div=table_div+"</tr></table></div>"



    if mod_num_votes[0]>mod_num_votes[1]:
        # print("BJP still wins by ",mod_num_votes[0]-mod_num_votes[1]," votes")
        table_div=table_div+"<div>"+"BJP still wins by "+str(mod_num_votes[0]-mod_num_votes[1])+"votes"+"</div>"
    else:
        # print("BJP loses by ",mod_num_votes[1]-mod_num_votes[0]," votes")
        table_div=table_div+"<div>"+"BJP loses by "+str(mod_num_votes[1]-mod_num_votes[0])+" votes"+"</div>"

    # print(table_div)

    mix_div=mix_div+graph_div+table_div



    #pitting top three against winner
    mod_parties=[]
    mod_parties.append(parties[0])
    mod_parties.append(parties[1]+" & "+parties[2]+" & "+parties[3])
    mod_num_votes=[]
    mod_num_votes.append(num_votes[0])
    mod_num_votes.append(num_votes[1]+num_votes[2]+num_votes[3])
    colors = ['rgba(104,204,204,1)']*len(mod_parties)
    colors[0]='rgba(221,104,94,1)'

    data = [go.Bar(
                x=mod_parties,
                y=mod_num_votes,
        marker=dict(
            color=colors),

        )]
    layout = go.Layout(
        title=state+' '+constituency+' 2014',
    )

    fig = go.Figure(data=data, layout=layout)
    #to create a div for the graph
    graph_div=plot(fig,output_type='div')


    table_div="<div><table><tr>"
    for party in mod_parties:
        table_div=table_div+"<th>"+str(party)+"<th>"
    table_div=table_div+"</tr><tr>"
    for vote in mod_num_votes:
        table_div=table_div+"<td>"+str(vote)+"<td>"
    table_div=table_div+"</tr></table></div>"



    if mod_num_votes[0]>mod_num_votes[1]:
        # print("BJP still wins by ",mod_num_votes[0]-mod_num_votes[1]," votes")
        table_div=table_div+"<div>"+"BJP still wins by "+str(mod_num_votes[0]-mod_num_votes[1])+" votes"+"</div>"
    else:
        # print("BJP loses by ",mod_num_votes[1]-mod_num_votes[0]," votes")
        table_div=table_div+"<div>"+"BJP loses by "+str(mod_num_votes[1]-mod_num_votes[0])+" votes"+"</div>"

    
    mix_div=mix_div+graph_div+table_div

    return mix_div









def analyze_constituency(state,district,constituency,df_results):
    # print(df_results.head())
    graph_div=""    
    #find the given constituency in that state
    df_results_districtwise=df_results[df_results["Constituency"]==constituency]

    #check if size is non 0
    num_of_candidates=df_results_districtwise.shape[0]
    if num_of_candidates == 0:
        f = open('missing.txt','a')
        f.write("#"+state+"#"+"X"+constituency+"X"+"\n")
        # f.write("X"+constituency+"X"+"\n")
        # print("X"+constituency+"X")
        f.close()
        return ""



    # print(df_results_districtwise.head())
    # print("Constituency is "+constituency+"***")
    df_results_districtwise_winner=df_results_districtwise[df_results_districtwise["Election Status"]=="Won"]
    
    if df_results_districtwise_winner.iloc[0]["Party"] in "BJP":
        # print("This is of interest")
        
        #Now sort the district wise result by vote count
        df_results_districtwise=df_results_districtwise.sort_values(by=['Count Of Votes'],ascending=False)
        
        winner_votes=int(df_results_districtwise_winner.iloc[0]["Count Of Votes"])
        num_votes=df_results_districtwise["Count Of Votes"].tolist()
        parties=df_results_districtwise["Party"].tolist()
        colors=[]
        colors = ['rgba(104,204,204,1)']*len(parties)
        colors[0]='rgba(221,104,94,1)'

        data = [go.Bar(
            x=parties,
            y=num_votes,
            marker=dict(
            color=colors),
    
    
            )]
        layout = go.Layout(
            title=state+' '+district+' '+constituency+' 2014',
        )

        fig = go.Figure(data=data, layout=layout)

        #to create a div for the graph
        graph_div=graph_div+plot(fig,output_type='div')

        margin=num_votes[0]-num_votes[1]
        # print("BJP won by ",margin," votes")

        #here we make the first table

        table_div="<div><table><tr>"
        for party in parties:
            table_div=table_div+"<th>"+str(party)+"<th>"
        table_div=table_div+"</tr><tr>"
        for vote in num_votes:
            table_div=table_div+"<td>"+str(vote)+"<td>"
        table_div=table_div+"</tr></table></div>"


        graph_div=graph_div+table_div


        #pitting top two against winner
        mod_parties=[]
        mod_parties.append(parties[0])
        mod_parties.append(parties[1]+" & "+parties[2])
        mod_num_votes=[]
        mod_num_votes.append(num_votes[0])
        mod_num_votes.append(num_votes[1]+num_votes[2])
        colors = ['rgba(104,204,204,1)']*len(mod_parties)
        colors[0]='rgba(221,104,94,1)'


        data = [go.Bar(
            x=mod_parties,
            y=mod_num_votes,
        marker=dict(
            color=colors),

        )]
        layout = go.Layout(
        title=state+' '+district+' '+constituency+' 2014',
        )

        fig = go.Figure(data=data, layout=layout)
        #to create a div for the graph
        graph_div=graph_div+plot(fig,output_type='div')
        
        table_div="<div><table><tr>"
        for party in mod_parties:
            table_div=table_div+"<th>"+str(party)+"<th>"
        table_div=table_div+"</tr><tr>"
        for vote in mod_num_votes:
            table_div=table_div+"<td>"+str(vote)+"<td>"
        table_div=table_div+"</tr></table></div>"



        if mod_num_votes[0]>mod_num_votes[1]:
            # print("BJP still wins by ",mod_num_votes[0]-mod_num_votes[1]," votes")
            table_div=table_div+"<div>"+"BJP still wins by "+str(mod_num_votes[0]-mod_num_votes[1])+" votes"+"</div>"
        else:
            # print("BJP loses by ",mod_num_votes[1]-mod_num_votes[0]," votes")
            table_div=table_div+"<div>"+"BJP loses by "+str(mod_num_votes[1]-mod_num_votes[0])+" votes"+"</div>"

        # print(table_div)

        graph_div=graph_div+table_div







        #pitting top three against winner
        mod_parties=[]
        mod_parties.append(parties[0])
        mod_parties.append(parties[1]+" & "+parties[2]+" & "+parties[3])
        mod_num_votes=[]
        mod_num_votes.append(num_votes[0])
        mod_num_votes.append(num_votes[1]+num_votes[2]+num_votes[3])
        colors = ['rgba(104,204,204,1)']*len(mod_parties)
        colors[0]='rgba(221,104,94,1)'

        data = [go.Bar(
                    x=mod_parties,
                    y=mod_num_votes,
            marker=dict(
                color=colors),

            )]
        layout = go.Layout(
            title=state+' '+district+' '+constituency+' 2014',
        )

        fig = go.Figure(data=data, layout=layout)
        #to create a div for the graph
        graph_div=graph_div+plot(fig,output_type='div')


        table_div="<div><table><tr>"
        for party in mod_parties:
            table_div=table_div+"<th>"+str(party)+"<th>"
        table_div=table_div+"</tr><tr>"
        for vote in mod_num_votes:
            table_div=table_div+"<td>"+str(vote)+"<td>"
        table_div=table_div+"</tr></table></div>"



        if mod_num_votes[0]>mod_num_votes[1]:
            # print("BJP still wins by ",mod_num_votes[0]-mod_num_votes[1]," votes")
            table_div=table_div+"<div>"+"BJP still wins by "+str(mod_num_votes[0]-mod_num_votes[1])+" votes"+"</div>"
        else:
            # print("BJP loses by ",mod_num_votes[1]-mod_num_votes[0]," votes")
            table_div=table_div+"<div>"+"BJP loses by "+str(mod_num_votes[1]-mod_num_votes[0])+" votes"+"</div>"

        
        graph_div=graph_div+table_div



    return graph_div


def analyze_constituency_by_district(state,district,year):

    
    district=district.strip()
    
    the_div=""

    constituencies=get_constituencies(state,district)
    df_results = pd.read_excel(state+".xlsx",sheet_name=year)

    for constituency in constituencies:
        the_div=the_div+analyze_constituency(state,district,constituency,df_results)

    return the_div



def generateGraphsAndData():
    

    muslim_pop_df=pd.read_excel("District-Constituency.xlsx")

    #strip spaces from columns
    muslim_pop_df= muslim_pop_df.rename(columns=lambda x: x.strip())

    # #now filter by % of population >25
    # muslim_pop_df=muslim_pop_df[muslim_pop_df["% of Total District Pop."]>25]

    # #sort by proportion of muslims
    # muslim_pop_df=muslim_pop_df.sort_values(by=['% of Total District Pop.'],ascending=False)

    # #ignore Kashmir as we are not analyzing it
    # muslim_pop_df = muslim_pop_df.drop(muslim_pop_df[muslim_pop_df.State =="J & Kashmir"].index)

    obtained_div=""
    for index,row in muslim_pop_df.iterrows():
        state=row["State"].strip()
        district=row["Districts"].strip()
        year="2014"

        if state!="Uttar Pradesh" and state!="Assam":
            obtained_div= obtained_div+ analyze_constituency_by_district(state,district,year)




    return obtained_div





def get_table_div(headers,values):
    table_div="<div><table><tr>"
    for header in headers:
        table_div=table_div+"<th>"+str(header)+"<th>"
    table_div=table_div+"</tr><tr>"
    for value in values:
        table_div=table_div+"<td>"+str(value)+"<td>"
    table_div=table_div+"</tr></table></div>"

    return table_div





def get_bar_graph_div(x,y,color_of_bars,title):
    data = [go.Bar(
        x=x,
        y=y,
        marker=dict(
        color=color_of_bars),
        )]

    layout = go.Layout(
        title=title,
    )

    fig = go.Figure(data=data, layout=layout)

    #to create a div for the graph
    g_div= plot(fig,output_type='div')
    # print("g_div",g_div)
    return g_div

def make_header_values_for_table(df,header_column,values_column,merge_factor):
    
    headers=df[header_column].tolist()
    values=df[values_column].tolist()
    if merge_factor!=0:
        merged_header=""
        merged_value=0
        for i in range(1,merge_factor+1):
            merged_header=merged_header+str(headers[i])
            merged_value=merged_value+values[i]
            del headers[i]
            del values[i]
        headers.insert(1,merged_header)
        values.insert(1,merged_value)

    return headers,values




def make_x_y_data_color_bar_graph(df,x_column,y_column,merge_factor):

    x=df[x_column].tolist()
    y=df[y_column].tolist()

    if merge_factor!=0:
        merged_y=0
        merged_x=""
        for i in range(1,merge_factor+1):
            merged_y=merged_y+y[i]
            merged_x=merged_x+str(x[i])
            del x[i]
            del y[i]
        x.insert(1,merged_x)
        y.insert(1,merged_y)




    colors=[]
    colors = ['rgba(104,204,204,1)']*len(x)
    colors[0]='rgba(221,104,94,1)'

    return x,y,colors






#merge_factor = 1 means no parties have merged
#merge_factor = 2 means 2nd and 3rd parties have merged
#merge_factor = 3 means 2nd. 3rd and 4th parties have merged
def get_graph_for_votes(df,state,district,constituency,year,merge_factor):
        
    x,y,colors=make_x_y_data_color_bar_graph(df,"Party","Count Of Votes",merge_factor)
    title='Const: '+constituency+' '+year
    graph_div=get_bar_graph_div(x,y,colors,title)
    return graph_div


    # headers,values=make_header_values_for_table(df,"Party","Count Of Votes",merge_factor)
    # table_div=get_table_div(headers,values)
    


def get_constituencies(state_name,district_name):
    # print(state_name," ",district_name)
    # dist_const_df = pd.read_excel("District-Constituency.xlsx")
    #strip spaces from columns
    global dist_const_df_total
    dist_const_df = dist_const_df_total.rename(columns=lambda x: x.strip())

    dist_const_df["State"] = dist_const_df["State"].str.strip()
    dist_const_df["Districts"] = dist_const_df["Districts"].str.strip()

    # print("sname=",state_name)

    dist_const_df = dist_const_df[dist_const_df["State"]==state_name]
    # print(dist_const_df)
    dist_const_df = dist_const_df[dist_const_df["Districts"]==district_name]
    dist_const_df = dist_const_df.reset_index(drop=True)

    if dist_const_df.empty:
        print("no match ",state_name,district_name)
        return None

    # print(dist_const_df)

    max_constituencies=10
    constituencies=[]
    for count in range(1,max_constituencies):
        col_name="Constituency"+str(count)
        if col_name in list(dist_const_df.columns.values):
            # print("looking for column",col_name)
            if pd.isnull(dist_const_df.at[0,col_name]) == False:
                constituencies.append(dist_const_df.at[0,col_name])
            else:
                break
        else:
            break

    return constituencies


def generate_graph_div_list_districtwise(state_name,district_name,constituencies,years):
    graph_div_const_year=[]
    for constituency in constituencies:
        # print("cons ",constituency)
        graph_div_year=[]
        for year in years:
            # df_result = pd.read_excel(state_name+".xlsx",sheet_name=year)

            df_result=all_vote_result_df[state_name][year]

            




            df_result_constituency=df_result[df_result["Constituency"]==constituency]
            # print(year)
            # print(df_result_constituency)
            #check if constituency not present in state file is non 0
            num_of_candidates=df_result_constituency.shape[0]
            if num_of_candidates == 0:
                f = open('missing.txt','a')
                f.write("#"+state_name+"#"+"X"+district_name+"X"+constituency+"X"+year+"\n")
                f.close()
                continue

            df_result_constituency=df_result_constituency.sort_values(by=['Count Of Votes'],ascending=False)
            

            merge_factor=0
            the_graph_div=get_graph_for_votes(df_result_constituency,state_name,district_name, constituency,year,merge_factor)
            graph_div_year.append(the_graph_div)


        graph_div_const_year.append(graph_div_year)
    return graph_div_const_year




def generate_data_for_district(state_name,district_name):
    

    constituencies=get_constituencies(state_name,district_name)
    print("const are",constituencies)
    if constituencies is None:
        return None
    
    years=['2014','2009','2004']
    graph_divs=generate_graph_div_list_districtwise(state_name,district_name,constituencies,years)

    return graph_divs
    
        






    






@app.route('/submit_form1', methods=[ 'POST'])
def give_graph():

    val="State: "+str(request.form['state'])+"</br>District: "+str(request.form['state_dist'])
    state=request.form['state'].strip()
    district=request.form['state_dist'].strip()
    full_div="<div><h2>"+val+"</h2></div>"

    whole_div=""
    graph_divs=generate_data_for_district(state,district)
    if graph_divs is None:
        whole_div =  "<div>No match for state "+state+" and district "+district+"</div>"
    else:
        whole_div='<div>'
        for i in range(len(graph_divs)):
            # print("div len is ",len(graph_divs[i]))
            width=int(100/len(graph_divs[i]))
            # print("width=",width)
            line_div='<div style="width: 100%;"><div style="float: left; width: '+str(width)+'%;">'
            for j in range(len(graph_divs[i])):
                # print("div is ",graph_divs[i][j])
                line_div=line_div+graph_divs[i][j]
                line_div=line_div+'</div><div style="float: left; width: '+str(width)+'%;">'
            line_div=line_div+'</div>'
            whole_div=whole_div+line_div
        whole_div=whole_div+"</div>"

    whole_div=full_div+whole_div




    return render_template('home.html',div_graph_placeholder=Markup(whole_div))

@app.route('/allbjp')
def get_all_BJP():

    year="2014"
    states=["West Bengal"]
    df=all_bjp[year]

    full_div=""
    for state in states:
        df_state=df[df["State"]==state]
        print(df_state.head())
        print(df_state["Constituency"].unique())
        for constituency in df_state["Constituency"].unique():
            df_state_constituency=df_state[df_state["Constituency"]==constituency]
            print(df_state_constituency)
            full_div=full_div+give_graph_table_div(df_state_constituency)


    # generate_data_for_district("Andhra Pradesh","Hyderabad")
    # full_div=generateGraphsAndData()
    # return "hello"
    # return render_template('home.html',div_graph_placeholder=Markup(full_div))
    # full_div="<div><h2>State, District</h2></div>"
    return render_template('all_bjp.html',div_graph_placeholder=Markup(full_div))
    # print("serving cold")
    # return render_template('allbjpstatic.html')




@app.route('/')
def start():
    # generate_data_for_district("Andhra Pradesh","Hyderabad")
    # full_div=generateGraphsAndData()
    # return "hello"
    # return render_template('home.html',div_graph_placeholder=Markup(full_div))
    full_div="<div><h2>State, District</h2></div>"
    return render_template('home.html',div_graph_placeholder=Markup(full_div))

if __name__=="__main__":
    main()
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port)
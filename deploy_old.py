from flask import Flask, render_template, request, Markup
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go
import pandas as pd

def main():
    print("At main, just once")

app = Flask(__name__)

app.config["DEBUG"]=True

def analyze_constituency(state,constituency,df_results):
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
            title=state+' '+constituency+' 2014',
        )

        fig = go.Figure(data=data, layout=layout)

        #to create a div for the graph
        graph_div=graph_div+plot(fig,output_type='div')

        margin=num_votes[0]-num_votes[1]
        print("BJP won by ",margin," votes")

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
        title=state+' '+constituency+' 2014',
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
            print("BJP still wins by ",mod_num_votes[0]-mod_num_votes[1]," votes")
            table_div=table_div+"<div>"+"BJP still wins by "+str(mod_num_votes[0]-mod_num_votes[1])+" votes"+"</div>"
        else:
            print("BJP loses by ",mod_num_votes[1]-mod_num_votes[0]," votes")
            table_div=table_div+"<div>"+"BJP loses by "+str(mod_num_votes[1]-mod_num_votes[0])+" votes"+"</div>"

        print(table_div)

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
            title=state+' '+constituency+' 2014',
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
            print("BJP still wins by ",mod_num_votes[0]-mod_num_votes[1]," votes")
            table_div=table_div+"<div>"+"BJP still wins by "+str(mod_num_votes[0]-mod_num_votes[1])+" votes"+"</div>"
        else:
            print("BJP loses by ",mod_num_votes[1]-mod_num_votes[0]," votes")
            table_div=table_div+"<div>"+"BJP loses by "+str(mod_num_votes[1]-mod_num_votes[0])+" votes"+"</div>"

        
        graph_div=graph_div+table_div



    return graph_div


        



def analyze_constituency_by_district(state,district,year):

    
    
    state_name_mapper={
    "Uttranchal":"Uttarakhand",
    "Pondichery":"Pondicherry"
    }
    if state in state_name_mapper.keys():
        state=state_name_mapper[state]
    print("reading ",state,".xlsx")
    df_results = pd.read_excel(state+".xlsx",sheet_name=year)

    district_constituency_mapper={
    "Maldah":["Maldaha Uttar","Maldaha Dakshin"],
    "Jyotiba Phule Nagar":["Amroha"],
    "Cachar":["Silchar"],
    "Darrang":["Mangaldoi"],
    "South  24 Parganas":["Diamond Harbour"],
    "Nadia":["Krishnanagar","Ranaghat"],
    "North East":["North East Delhi"],
    "Central":["Chandni Chowk"],
    "Balrampur":["Shrawasti"],
    "Uttar Dinajpur":["Raiganj"],
    "Sahibganj":["Rajmahal"],
    }

    #get all constituencies according to given district
    constituencies=[]
    district=district.strip()
    # print("District is "+district+"***")
    if district in district_constituency_mapper.keys():
        constituencies=district_constituency_mapper[district]
    else:
        constituencies.append(district.strip())

    the_div=""

    for constituency in constituencies:
        the_div=the_div+analyze_constituency(state,constituency,df_results)

    return the_div







def generateGraphsAndData():
    muslim_pop_df=pd.read_excel("District_muslim_Population-2001.xls")

    #strip spaces from columns
    muslim_pop_df= muslim_pop_df.rename(columns=lambda x: x.strip())

    #now filter by % of population >25
    muslim_pop_df=muslim_pop_df[muslim_pop_df["% of Total District Pop."]>25]

    #sort by proportion of muslims
    muslim_pop_df=muslim_pop_df.sort_values(by=['% of Total District Pop.'],ascending=False)

    #ignore Kashmir as we are not analyzing it
    muslim_pop_df = muslim_pop_df.drop(muslim_pop_df[muslim_pop_df.State =="J & Kashmir"].index)

    obtained_div=""
    for index,row in muslim_pop_df.iterrows():
        state=row["State"]
        district=row["Districts"]
        year="2014"

        obtained_div= obtained_div+ analyze_constituency_by_district(state,district,year)




    return obtained_div



@app.route('/')
def start():
    full_div=generateGraphsAndData()
    # return "hello"
    return render_template('home.html',div_graph_placeholder=Markup(full_div))

if __name__=="__main__":
    main()
    app.run(host='0.0.0.0',port=5000)
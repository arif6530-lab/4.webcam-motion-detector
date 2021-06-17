#Explaination
#step1-we will import df from ColoredMotionDetector.py
#step2-we will plot a quad chart 
#step3-we will use hover tool so that when we put cursor on graph,it will show entry and exit time.


from ColoredMotionDetector import df    #importing data frame from MotionDetector.py
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import HoverTool, ColumnDataSource   #used to create a hover window


df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")  #we are making a new column and storing start time in str format, then we will attach it to hover-bcoz hover was not accepting default datetime format
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")  #same (End time)
cds=ColumnDataSource(df) #imp for hover window

f=figure(width=500,height=300,x_axis_type="datetime",title="Motion Detector") #for representing date on x axis we use x_axis-type="datetime"
f.xaxis.axis_label="Motion Detecting Line"
f.axis.minor_tick_line_color=None
f.yaxis[0].ticker.desired_num_ticks=1  #this will remove grids from chart

hover=HoverTool(tooltips=[("Begining","@Start_string"),("Ending","@End_string")]) #here @ mean , cds will autoamtically fetch data from these coulmns
f.add_tools(hover) #adding hover on graph


q=f.quad(top=1,bottom=0,left="Start",right="End", color="green",source=cds) #source=cds is imp for hover to work   
#left=df["start"] means when object tracking starts ,quad should also start, 
#right=df["End"]  means when tracking ends quad should also end
#note- we used source=cds  bcoz of this in line 26 , df["Start"] sould be replaced with Start, and df["End"] with End,otherwise it will give error
output_file("bokehChart.html")
show(f)
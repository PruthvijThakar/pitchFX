import os
import xml.etree.ElementTree as ET
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
thread_sleep = 2


# waling through given folders and files for getting targetted information 
def extract_atbat(path):
    atbat = []
    
    xmlfiles = [os.path.join(root, name)
             for root, dirs, files in os.walk(path)
             for name in files
             if name.endswith(("inning.xml"))]
    for f in xmlfiles:
        try:
            tree = ET.parse(str(f))
            root = tree.getroot()
            for child in root: 
                parser_atbat = child.iter('atbat')
                for at_bat in parser_atbat:
                    atbat.append(at_bat)
        except ET.ParseError:
            print ("Something went wrong while parsing " + f)

    return atbat
#getting last 3 pitches
def wanted_pitches(at_bat):
    pitches = list(at_bat.iter('pitch'))
    if len(pitches) >= 3:
        return pitches[len(pitches) - 3:]

#binning the pitch types wanted
def get_dict_key(pitch_types):
    pitch_dict = [None] * len(pitch_types)
    for i in range(0, len(pitch_types)):
        p_type = pitch_types[i].get('pitch_type')
        extracted_pitches = pitch_type_bins(p_type) 
        pitch_dict[i] = extracted_pitches 
    return tuple(pitch_dict)

#converting abbreveations in actual meaning
def pitch_type_bins(pitch_type):

    fastballs = ['FT', 'FF', 'FA', 'FS']
    curveballs = ['CU', 'CB']
    sliders = ['SL']

    if pitch_type in fastballs:
        return 'FAST'
    elif pitch_type in curveballs:
        return 'CURVE'
    elif pitch_type in sliders:
        return 'SLIDER'
    else:
        return None

# Finding categeories from sub categories
def get_event_atbat(at_bat):

    events_atbat = at_bat.get('event')

    Hit = ['Hit', 'Single', 'Double', 'Triple', 'Home Run', 'Bunt']
    Hit_out = ['Groundout', 'Flyout', 'Foul Out']
    Strikeout = ['Strikeout', 'Swinging', 'Looking']
    Walk = ['Walk']
    
    if events_atbat in Hit:
        return 'Hit'
    elif events_atbat in Hit_out:
        return 'Hit_out'
    elif events_atbat in Strikeout:
        return 'Strikeout'
    elif events_atbat in Walk:
        return 'Walk'
    else:
        return 'Other'

# creating final dict with a counter of each events for a 
def atbat_final(ab, events_dict):
    for at_bat in ab:
        pitch_seq = wanted_pitches(at_bat)
        events_atbat = get_event_atbat(at_bat) 

        if pitch_seq is not None:
            at_bat_key = get_dict_key(pitch_seq)
            if None not in at_bat_key:
                if at_bat_key not in events_dict:
                    events_dict[at_bat_key] = {'Hit': 0, 'Hit_out': 0, 'Strikeout': 0, 'Walk': 0, 'Other': 0}

                results_breakdown_dict = events_dict[at_bat_key] 
                if events_atbat is not None:
                    results_breakdown_dict[events_atbat] += 1

# combining the input sequences and comparing it with available sequences
def final_pitches():
 
    valid_inputs = [['FAST', 'FAST', 'CURVE'], ['FAST', 'FAST', 'FAST'],['FAST', 'SLIDER' ,'SLIDER'], ['SLIDER', 'FAST', 'SLIDER']]
    
    input_list = input("Please input the pattern you want to visualize: ")
    pitches_ip = input_list.split() #splits the input string on spaces
    pitch = [str(a) for a in pitches_ip] 
    
    if pitch in valid_inputs:
        pitch1 = pitch[0]
        pitch2 = pitch[1]
        pitch3 = pitch[2]
        combined_pitch = (pitch1, pitch2, pitch3)
        return combined_pitch
    else:    
        print ("invalid pattern")
    
# plotting charts from obtained dict
def view_charts(pK, finaldict): 
    categorized_events = finaldict[pK]
    category_counts = (categorized_events['Walk'], categorized_events['Strikeout'], categorized_events['Hit'], categorized_events['Hit_out'], categorized_events['Other']) 
    bins = len(categorized_events)
    i = np.arange(bins)
    plots = plt.bar(i, category_counts)
    plt.xlabel('Events')
    plt.ylabel('Count')
    plt.title('Results for sequence \n ' + pK[0] + ', ' + pK[1] + ', ' + pK[2], fontsize=12)
    plt.xticks(i+0.8/2,('Walk', 'Strikeout', 'Hit', 'Hit (out)', 'Other'))
    plt.show()
    
# invoking functions and specifying path to be extracted     
def combine_functions():
 
    ab = extract_atbat("C:\\Users\\pruth\\Desktop\\CSYE 7245\\NeuroScouting\\2013_pitchfx_data\\2013_pitchfx_data") # Enter path to your folder storage
    sleep(thread_sleep)
    events_dict = {}
    atbat_final(ab, events_dict)
    return events_dict

# callable function for main method
def generate_output():

    events_dict = combine_functions()             
    combined_pitch = final_pitches()   
    view_charts(combined_pitch, events_dict)  
    
if __name__ == "__main__":
    generate_output()
    

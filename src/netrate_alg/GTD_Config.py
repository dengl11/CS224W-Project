###################################
# Configuration of GTD Dataset 
###################################
import sys
sys.path.append("lib")
import pickle
import os 
from dataframe_preprocessor import DataframePreprocessor

gtd_file_name = 'globalterrorismdb_0617dist.csv'
# path of full gtd csv file 
gtd_path = os.path.join(os.getcwd(), "../../data/GTD/{}".format(gtd_file_name))
mapping_path = os.path.join(os.getcwd(), "../../data/GTD/generated/column_mapping.pkl")

########## Column Name ##############

# selected_cols = ['iyear','imonth','iday','country_txt','region_txt','provstate','city','latitude','longitude','attacktype1_txt','targtype1_txt','gname','weaptype1_txt','nkill','nwound'] 

COL_year = "iyear"
COL_month = "imonth"
COL_lat = "latitude"
COL_log = "longitude"
COL_gname = "gname"
COL_country = "country"
COL_country_txt = "country_txt"
COL_nkill = "nkill"
COL_nwound = "nwound"
COL_eventid = 'eventid'
COL_attacktype1 = 'attacktype1'
COL_targtype1 = 'targtype1'
COL_weapsubtype1 = 'weapsubtype1'
COL_success = 'success'
COL_suicide = 'suicide'
COL_nperps = 'nperps'
COL_related = 'related'



########## Group Name ##############
GROUP_ISIL = "Islamic State of Iraq and the Levant (ISIL)"
GROUP_Taliban = "Taliban"
GROUP_SL = "Shining Path (SL)"
GROUP_FMLN = "Farabundo Marti National Liberation Front (FMLN)"
GROUP_Al = "Al-Fatah"
GROUP_IRA = "Irish Republican Army (IRA)"
GROUP_FARC = "Revolutionary Patriotic Anti-Fascist Front (FRAP)"
GROUP_NPA = "New People's Army (NPA)"
GROUP_PKK = "Kurdistan Workers' Party (PKK)"
GROUP_BOKO = "Boko Haram"


def get_full_gtd():
    """return dataframe preprocessor for full GTD Dataset 
    Return: 
    """
    return DataframePreprocessor.init_from_file(gtd_path, index_col = COL_eventid)

def get_column_map():
    """return the mapping of columns 
    Return: 
    """
    # load mapping 
    with open(mapping_path, "rb") as f:
        column_map = pickle.load(f)
    return column_map 

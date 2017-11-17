# CS224W-Project

### Team

- Julia Alison (jalison@stanford.edu)
- Li Deng (dengl11@stanford.edu)
- Zheqing (Bill) Zhu (zheqzhu@stanford.edu)

--------------------------


Timeline

10/24 Tuesday night 8 pm homework discussion

10/29 Sunday morning 10 am: 

Bill finish data compilation for both group network. 

Julia read more about cascading patterns of organizations, especially look for temporal survival pattern.

Li study more about group interaction under the setting of event network, build hypotheses and develop theories. 

Julia and Li please implement your methods on a null model while Bill is compiling data.

11/12 Sunday Morning 10 am:

Update with algorithm and implementation details and results.

Data:

gtd_graph_by_year.txt stores a network where each event id is grouped by year of occurrence. All events that conducted by the same group and in the same year form a complete network. 

gtd_graph_by_year_month.txt stores a similar network as gtd_graph_by_year except that it forms complete graphs by month.

raw_gtd_data.pkl is a list of all events with details

gtd_group_dict.pkl is the same structure gtd_graph_by_year_month, but mapped to dictionary. Access the dictionary like this: gtd_group_dict[group_name][year][month].

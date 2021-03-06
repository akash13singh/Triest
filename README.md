# TRIEST

Implementation and evaluation of paper: 
<a href="http://www.kdd.org/kdd2016/subtopic/view/triest-counting-local-and-global-triangles-in-fully-dynamic-streams-with-fi">
TRIEST: Counting Local and Global Triangles in Fully-Dynamic Streams with Fixed Memory Size</a>

We implement the first two algorithms in the paper :  
TRIEST-BASE  
TRIEST-IMPR  

# Notes:

1) We assume working with directed graphs only as the paper also mentions delaing with undirected graphs in section 2 (Preliminaries). We extend the algorithm to handle directed graphs. We process every edge (u,v) such that:
   u  <  v
   u  !=  v 
   Discard edges (u,u)
  If edge (u,v) is already present in the current edge sample S, we discard (u,v) or (v,u). 
 Evaluation with Advogato dataset, a directed graph gave good results with this handling.

2) In evaluation we compare only the global triangles count as the test datasets provided the true value of only global triangle counts.  However the code outputs the values of local Ts and Eta for Triest-Base, and the local triangle estimates for Triest-Impr.

# Execution Instructions:

1) Run scripts triest_impr.py for Triest-Impr algorithm and triest_base for Triest-Base
   algorithm.  
2) The desired dataset and values of M can be set in variables datafile and M
   respectively in the main() method of either script.  
3) The code assumes that the first two columns of the datafile are in the form: \<source_node> \<destination_node>.  
4) The code works with space separated files and works with only the first two fields of each row and ignores the rest.  

# Datasets:
1) The code was evaluated on 3 datasets present in the [data](/data) folder.  
2) More graph datasets can be obtained from [here](http://konect.uni-koblenz.de/).  

# Results & Evaluation:
1) Both algorithms converge to the correct value at M =40,000 but give good estimates  even with much lower values of M.</br>
        *Triest Evaluation on Advogato dataset.*
   ![Triest-Base](evaluation/triest_base_advogato.png) 
   ![Triest-Impr](evaluation/triest_impr_advogato.png)             
2) The full evaluation and results are present in the [report](evaluation/triest_report.pdf).

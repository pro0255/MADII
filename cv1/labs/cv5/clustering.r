# https://igraph.org/c/doc/igraph-Community.html 


if (!require("igraph")) 
  install.packages("igraph")
library(igraph)
if (!require("ggplot2")) 
  install.packages("ggplot2")
library(ggplot2)


#g = make_graph("Zachary") # nacti Karate club


KarateClub = "C:\\Users\\Vojta\\Desktop\\own\\university\\ing\\01\\madII\\datasets\\KarateClub.csv"

KNN = "C:\\Users\\Vojta\\Desktop\\own\\university\\ing\\01\\madII\\datasets\\knn3.csv"

radius = "C:\\Users\\Vojta\\Desktop\\own\\university\\ing\\01\\madII\\datasets\\radius1.csv"

combination = "C:\\Users\\Vojta\\Desktop\\own\\university\\ing\\01\\madII\\datasets\\combination3,1.csv"


output <- "C:\\Users\\Vojta\\Desktop\\own\\university\\ing\\01\\madII\\outputs\\cv5\\karateclub.csv"
f <- KarateClub
# nacteni dat do dataframu
df <- read.csv2(f, header =TRUE, stringsAsFactors=F)
dim(df)
#df$WEIGHT<- NULL, pokud byste meli i sloupec s vahami hran
# prevod na objekt "typu" igraph
g <- graph.data.frame(df, directed = FALSE) 

g # nebo print(g)

coords = layout_with_fr(g) 
plot(g, layout=coords, vertex.label=NA, vertex.size=10)

############################
# greedy method (hiearchical, fast method)
c1 = cluster_fast_greedy(g)



#all cluster data
##### START #####
fast_greedy = cluster_fast_greedy(g)
edge_betweenness = cluster_edge_betweenness(g)
louvain = cluster_louvain(g)	
optimal = cluster_optimal(g)	
label_prop = cluster_label_prop(g)

fast_greedy_membership <- membership(fast_greedy)
edge_betweenness_membership <- membership(edge_betweenness)
louvain_membership <- membership(louvain)
optimal_membership <- membership(optimal)
label_prop_membership <- membership(label_prop)



emp.data <- data.frame(
  fast_greedy = as.numeric(fast_greedy_membership),
  edge_betweenness = as.numeric(edge_betweenness_membership),
  louvain = as.numeric(louvain_membership),
 optimal = as.numeric(optimal_membership),
  label_prop = as.numeric(label_prop_membership)
)

write.csv2(emp.data, file = output, row.names = TRUE)
##### END #####



v <- membership(c1)
print(v)
#length(c1)
#sizes(c1)
#crossing(c1, g)

s <- (table(as.numeric(sizes(c1))))

plot(c1, g, layout=coords) 
plot(g, vertex.color=membership(c1), layout=coords) # vyexportujte
#plot_dendrogram(c1) # vyexportujte

df2 <- data.frame(velikost=as.numeric(names(s)),freq=as.numeric(s)) 
p <- ggplot(df2, aes(x = velikost)) + 
  geom_histogram(binwidth = 0.5) +
  scale_x_continuous(breaks = seq(0, max(df2$velikost)+2,1 ), lim = c(0, max(df2$velikost)+2)) + 
  #  scale_x_discrete() +
  # scale_y_discrete() +
  theme_bw()
print(p)

# nebo treba
p <- ggplot(df2, aes(x = velikost, y = freq)) + 
  geom_point() + 
  scale_x_continuous(breaks = pretty(df2$velikost, n = max(df2$velikost)-min(df2$velikost))) +
  scale_y_continuous() +
  theme_bw()

print(p)
# ulozime do pdf
#pdf(file = "distr_vel_komunit.pdf")
#plot(p)
#dev.off()

# zapiseme id vrcholu a id komunit ke kterym prislusi
write.csv2(as.numeric(v), file = output, row.names = TRUE)

############################
# dalsi metody alespo tyto
# cluster_edge_betweenness
# cluster_louvain	
# cluster_optimal	
# cluster_label_prop

############################
# tyto nejsou nutne
# cluster_infomap	
# cluster_leading_eigen

#####################################
#####################################








































# hierarchicke shlukovani

S=similarity(g, method = "invlogweighted")  
D = 1-S

# vyzkousejte i dalsi metody pro vypocet podobnosti

# distance object
d = as.dist(D)

# average-linkage clustering method
cc = hclust(d, method = "average")

# plot dendrogram
plot(cc)

# draw blue borders around clusters
clusters.list = rect.hclust(cc, k = 3, border="blue") 

# cut dendrogram at 3 clusters
clusters = cutree(cc, k = 3)

plot(g, vertex.color=clusters, layout=coords)

#######################################
import cPickle as pickle
import sys
import logging

### build graph: 
### takes as input a file in the form:
## a b dist time
### where a and b are destinations, dist is the distance between them, and 
### time is the time needed to travel between them and constructs a graph.

### This graph should be represented as an adjacency list, and stored as a 
### dictionary, with the key in the dictionary being the source, and
### the value being a list of edges with that source.  The graph should
### be undirected -- so that each edge (a,b) should appear in the adjecency
### list for a *and* the adjacency list for b.

class graph():
    def __init__(self, infile=None):
        self.adjlist = {}
        if infile:
            self.buildGraph(infile)


    ### method to print a graph.
    def __repr__(self):
        result = ''
        for v in self.adjlist:
            result = result + v.name + ': '
            for e in self.adjlist[v][:-1]:
                result = result + e.dest + ', '
            result = result + self.adjlist[v][-1].dest
            result += '\n\n'
        return result

    ### helper methods to construct edges and vertices. Use these in buildGraph.
    def createVertex(self, str):
        name, lat, long = str.split(" ", 2)
        lat = lat.split("=")[1]
        long = long.split("=")[1]
        return location(name, lat, long)

    def createEdges(self, str):
        src, dest, dist, time = str.split(" ", 4)
        dist = dist.split("=")[1]
        time = time.split("=")[1]
        e1 = edge(src, dest, dist, time)
        e2 = edge(dest, src, dist, time)

        #TODO: it seems the return statement is missed
        return [e1, e2]

    ### method that takes as input a file name and constructs the graph described
    ### above.
    def buildGraph(self, infile):
        f = open(infile)
        isEdges = False
        for line in f:
            if not isEdges:
                if '## edges' in line:
                    isEdges = True
                elif '##' in line:
                    pass
                else:
                    v = self.createVertex(line)
                    self.adjlist[v] = []
            else:
                edges = self.createEdges(line)
                for e in edges:
                    for v in self.adjlist.keys():
                        if v.name == e.src:
                            self.adjlist[v].append(e)
                            break

        f.close()


    ### This method should compute Dijskta's algorithm.  It should return a
    ### dictionary where the key is the destination vertex, and the value is
    ### a tuple consisting of the cost of the path an a list of vertices
    ### that make up the path from the source to the destination
    def dijkstra(self, start):
        dist = {}
        pre = {}
        for v in self.adjlist.keys():
            if v.name == start:
                dist[v] = 0
                pre[v] = None
            else:
                dist[v] = float('inf')
                pre[v] = None
        q = list(self.adjlist.keys())

        while len(q) != 0:
            nearest = None

            for i in sorted(dist.items(), key=lambda x: x[1]):
                if i[0] in q:
                    nearest = i[0]
                    break
            q.remove(nearest)

            if dist[nearest] == float('inf'):
                break

            for e in self.adjlist[nearest]:
                adjacency = None
                for v in self.adjlist.keys():
                    if v.name == e.dest:
                        adjacency = v
                        break

                alt = dist[nearest] + float(e.distance[:-2])
                if alt < dist[adjacency]:
                    dist[adjacency] = alt
                    pre[adjacency] = nearest

        result = {}

        for v in self.adjlist.keys():
            # Construct the path
            path = []
            current = v

            while True:
                path.insert(0, current)
                current = pre[current]
                if current is None:
                    break
            if len(path) > 0:
                result[v] = tuple((dist[v], path))
        return result

### classes representing locations and edges

class location():
    def __init__(self, name, lat, longitude):
        self.name = name
        self.lat = lat
        self.longitude = longitude

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class edge():
    def __init__(self, src, dest, distance, time):
        self.src = src
        self.dest = dest
        self.distance = distance
        self.time = time


### usage: buildGraph {--pfile=outfile} {-p} infile
### if --pfile=outfile is provided, write a pickled version of the graph 
### to outfile. Otherwise, print it to standard output.
### if --prim, compute prim

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    dijkstra = None
    pfile = None

    if len(sys.argv) > 1:
        for arg in sys.argv[1:-1]:
            if arg.startswith('--dijkstra='):
                logging.debug('dijkstra')
                dijkstra = arg[11:]
            elif arg.startswith('--pfile='):
                logging.debug('pfile')
                pfile = arg[8:]
            else:
                print('Usage: buildGraph {--pfile=outfile} {--dijkstra=start} infile')
                exit()
    else:
        print('Usage: buildGraph {--pfile=outfile} {--dijkstra=start} infile')
        exit()

    gr = graph(sys.argv[-1])

    if pfile is not None:
        f = open(pfile, 'w')
        pickle.dump(gr, f)
        f.close()
    else:
        print '-----Adjacent list of the graph-----'
        print repr(gr)

    if dijkstra is not None:
        print '-----Start location----- '
        print dijkstra
        print

        result = gr.dijkstra(dijkstra)
        print '-----dijkstra result-----'
        for r in result.items():
            s = r[0].name
            s = s + ', cost=' + str(r[1][0])
            s += ', path:{'
            for v in r[1][1][:-1]:
                s = s + v.name + '->'
            s = s + r[1][1][-1].name + '}'
            print s
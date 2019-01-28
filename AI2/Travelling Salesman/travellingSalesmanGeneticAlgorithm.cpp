#include <bits/stdc++.h>
using namespace std;

/* Explanation:
Chromosome: bool array where array[i] = true means the i-th edge will be present
Fitness: -inf if (verticesOcurrences != 2) for any vertex else -(sum of edge costs)
Crossing: switch an edge from u with an edge from v
Mutation: switch an edge for another
Selection: sort chromosomes and choose the 0.8 best
Substitution: only the best between new and old population
*/

const int populationSize = 100, selectedToMate = 50;

vector<pair<int, int>> graph[(int) 1e6]; int edges[(int) 1e6][3];
int n, m; double inf = 1e9;

struct Chromosome
{
  double fitness;
  vector<bool> hasEdge;
  bool operator<(const Chromosome &a) const { return(fitness < a.fitness); }
  bool operator==(const Chromosome &a) const
  {
    if (fitness != a.fitness) return(false);
    for (int i = 0; i < m; i ++) if (hasEdge[i] != a.hasEdge[i]) return(false);
    return(true);
  }
};

struct Population
{
  vector<Chromosome> chromosomes;
  void calculateFitness()
  {
    int verticesCount[n];
    for (Chromosome &c: chromosomes)
    {
      memset(verticesCount, 0, sizeof(verticesCount));
      c.fitness = 0; int ec = 0;
      for (int i = 0; i < m; i ++) if (c.hasEdge[i]) verticesCount[edges[i][0]] ++, verticesCount[edges[i][1]] ++, c.fitness -= edges[i][2], ec ++;
      if (ec != n) printf("THAT'S SOMETHING WRONG IN YOUR OPERATIONS\n");
      for (int i = 0; i < n; i ++) if (verticesCount[i] != 2) c.fitness = -inf;
      // if (c.fitness != -inf) { printf("YaY\n"); exit(0); }
    }
    sort(chromosomes.begin(), chromosomes.end());
  }
  void merge(Population &newPopulation)
  {
    for (int i = populationSize - 1, j = selectedToMate - 1; i >= 0 && j >= 0; i --)
      if (chromosomes[i].fitness <= newPopulation.chromosomes[j].fitness)
        chromosomes[i] = newPopulation.chromosomes[j --];
    sort(chromosomes.begin(), chromosomes.end());
  }
};

int main()
{
  srand(time(NULL));
  scanf("%d %d", &n, &m);
  for (int i = 0, u, v, c; i < m; i ++)
  {
    scanf("%d %d %d", &u, &v, &c); u --, v --;
    graph[u].push_back({v, c}), graph[v].push_back({u, c});
    edges[i][0] = u, edges[i][1] = v, edges[i][2] = c;
  }

  Population population; population.chromosomes.resize(populationSize);
  for (Chromosome &c: population.chromosomes)
  {
    c.hasEdge.resize(m);
    for (int edgeSum = 0; edgeSum < n; edgeSum ++)
    {
      int position = rand() % m;
      while (c.hasEdge[position]) position = rand() % m;
      c.hasEdge[position] = true;
    }
  }
  population.calculateFitness();

  for (int repetitions = 0; repetitions < 10000;)
  {
    Chromosome prevBest = population.chromosomes[populationSize - 1];
    printf("repetions: %d, bestFitness: %lf | ", repetitions, prevBest.fitness);
    for (int i = 0; i < m; i ++) printf("%d", (int) prevBest.hasEdge[i]); printf("\n");

    Population newPopulation;
    for (int i = 0; i < selectedToMate; i ++) newPopulation.chromosomes.push_back(population.chromosomes[populationSize - selectedToMate + i]);
    for (int i = 0; i < selectedToMate; i ++)
    {
      int u = 0, v = 0;
      while (u == v) u = rand() % selectedToMate, v = rand() % selectedToMate;
      for (int j = 0; j < 1; j ++) // crossing
      {
        int position = rand() % m, other = rand() % m, tries = 0;
        while (tries ++ < 1000 && (newPopulation.chromosomes[u].hasEdge[position] == newPopulation.chromosomes[u].hasEdge[other] || newPopulation.chromosomes[v].hasEdge[position] == newPopulation.chromosomes[v].hasEdge[other])) position = rand() % m, other = rand() % m;
        if (tries < 1000)
          swap(newPopulation.chromosomes[u].hasEdge[position], newPopulation.chromosomes[v].hasEdge[position]),
          swap(newPopulation.chromosomes[u].hasEdge[other], newPopulation.chromosomes[v].hasEdge[other]);
      }
      for (int j = 0; j < 1; j ++) // mutation
      {
        int position = rand() % m, other = rand() % m, tries = 0;
        while (tries ++ < 1000 && newPopulation.chromosomes[u].hasEdge[position] == newPopulation.chromosomes[u].hasEdge[other]) position = rand() % m, other = rand() % m;
        if (tries < 1000)
          newPopulation.chromosomes[u].hasEdge[position].flip(), newPopulation.chromosomes[u].hasEdge[other].flip();
        position = rand() % m, other = rand() % m, tries = 0;
        while (tries ++ < 1000 && newPopulation.chromosomes[v].hasEdge[position] == newPopulation.chromosomes[v].hasEdge[other]) position = rand() % m, other = rand() % m;
        if (tries < 1000)
          newPopulation.chromosomes[v].hasEdge[position].flip(), newPopulation.chromosomes[v].hasEdge[other].flip();
      }
    }
    newPopulation.calculateFitness();
    population.merge(newPopulation);
    if (population.chromosomes[populationSize - 1] == prevBest) repetitions ++;
    else repetitions = 0;
  }
  printf("cost: %lf | ", population.chromosomes[populationSize - 1].fitness);
  for (int i = 0; i < m; i ++) printf("%d", (int) population.chromosomes[populationSize - 1].hasEdge[i]); printf("\n");

  return(0);
}
#include <bits/stdc++.h>
#define VERBOSE if(0)
using namespace std;

/* Explanation:
Chromosome: int array of values for each variable
Fitness: how distant the calculated value is from the objective value
Crossing: No crossing
Mutation: randomly select a position to add a random value from 0 to 9
(multiplied by -1 according to if the calculated value if bigger then the objective value
of if the constant on that position is negative)
Selection: sort chromosomes and choose the 0.5 best
Substitution: only the best between new and old population
*/

const int populationSize = 10, toMate = 5;

int c[(int) 1e6], y, n;

struct Chromosome
{
  double fitness; int y;
  vector<int> x;
  bool operator<(const Chromosome &a) const { return(fitness < a.fitness); }
  bool operator==(const Chromosome &a) const
  {
    if (fitness != a.fitness) return(false);
    for (int i = 0; i < n; i ++) if (x[i] != a.x[i]) return(false);
    return(true);
  }
};

struct Population
{
  vector<Chromosome> chromosomes;
  void calculateFitness()
  {
    for (Chromosome &chromosome: chromosomes)
    {
      chromosome.y = 0;
      for (int i = 0; i < n; i ++) chromosome.y += c[i] * chromosome.x[i];
      chromosome.fitness = -abs(y - chromosome.y);
    }
    sort(chromosomes.begin(), chromosomes.end());
  }
  void substitute(Population &newPopulation)
  {
    for (int i = populationSize - 1, j = toMate - 1; i >= 0 && j >= 0; i --)
      if (newPopulation.chromosomes[j].fitness > chromosomes[i].fitness)
        chromosomes[i] = newPopulation.chromosomes[j --];
    
  }
};

int main()
{
  srand(time(NULL));
  scanf("%d", &n);
  for (int i = 0; i < n; i ++) scanf("%d", &c[i]);
  scanf("%d", &y);

  Population population; population.chromosomes.resize(populationSize);
  for (Chromosome &chromosome: population.chromosomes)
  {
    chromosome.x.resize(n);
    for (int i = 0; i < n; i ++) chromosome.x[i] = rand() % 2001 - 1000;
  }
  population.calculateFitness();

  for (int repetitions = 0; repetitions < 10000;)
  {
    Chromosome prevBest = population.chromosomes[populationSize - 1];
    VERBOSE
    {
      printf("repetitions: %d, fitness: %lf | ", repetitions, prevBest.fitness);
      for (int i = 0; i < n; i ++) printf("%d*%d ", c[i], prevBest.x[i]); printf("= %d\n", prevBest.y);
    }

    Population newPopulation;
    for (int i = 0; i < toMate; i ++) newPopulation.chromosomes.push_back(population.chromosomes[populationSize - toMate + i]);

    for (int i = 0; i < toMate; i ++) // mutation
    {
      for (int j = 0; j < 1; j ++)
      {
        int position = rand() % n, dx = rand() % 10;
        newPopulation.chromosomes[i].x[position] += (newPopulation.chromosomes[i].y < y ? 1 : -1) * (c[position] > 0 ? 1 : -1) * dx;
      }
    }

    newPopulation.calculateFitness();
    population.substitute(newPopulation);

    if (prevBest.fitness == 0) break;
    if (prevBest == population.chromosomes[populationSize - 1]) repetitions ++;
    else repetitions = 0;
  }
  Chromosome best = population.chromosomes[populationSize - 1];
  printf("fitness: %lf | ", best.fitness);
  for (int i = 0; i < n; i ++) printf("%d*%d ", c[i], best.x[i]); printf("= %d\n", best.y);

  return(0);
}
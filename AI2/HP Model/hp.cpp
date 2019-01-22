// #include <bits/stdc++.h>
#include <vector>
#include <queue>
#include <set>
#include <algorithm>
#include <string.h>
using namespace std;

int hpSize; char hp[(int) 1e6]; double baseEnergy = 0, accumulatedEnergy[1000];
int dx[4] = {0, 1, 0, -1}, dy[4] = {1, 0, -1, 0}, n, m, si, sj;
char dop[4 + 1] = {'v', '>', '^', '<'}, table[1000][1000];

struct State
{
  vector<char> direction;
  int i = 0, j = 0;
  set<pair<int, int>> hVisited, pVisited;
  double value = 0, energy = 0;
  bool operator<(const State &b) const { return(value > b.value); }
  void insert(pair<int, int> position, char protein) { if (protein == 'P') pVisited.insert(position); else hVisited.insert(position); i = position.first, j = position.second; }
  bool has(pair<int, int> position) { return(hVisited.count(position) || pVisited.count(position)); }
};
void fillTable(State &state)
{
  int minI = 0, maxI = 0, minJ = 0, maxJ = 0;
  int i = 0, j = 0;
  for (auto d: state.direction)
  {
    i += dy[d], j += dx[d];
    minI = min(minI, i), maxI = max(maxI, i), minJ = min(minJ, j), maxJ = max(maxJ, j);
  }
  n = maxI - minI + 1, m = maxJ - minJ + 1;
  for (int i = 0; i < n; i ++) { for (int j = 0; j < m; j ++) table[i][j] = '.'; table[i][m] = '\0'; }
  i = -minI, j = -minJ; si = i, sj = j; int s = 0;
  table[i][j] = hp[s ++];
  for (auto d: state.direction)
  {
    i += dy[d], j += dx[d];
    table[i][j] = hp[s ++];
  }
}
double stateEnergy(State &state, bool fill)
{
  if (fill) fillTable(state);
  double energy = baseEnergy;
  for (int i = 0; i < n; i ++)
    for (int j = 0; j < m; j ++)
      if (table[i][j] == 'H')
      {
        energy -= (i + 1 < n) && table[i + 1][j] == 'H';
        energy -= (j + 1 < m) && table[i][j + 1] == 'H';
      }
  return(energy);
}
void printState(State &state)
{
  printf("------------------------------\n");
  fillTable(state);
  for (int d = 0; d < state.direction.size(); d ++)
    printf("%c%c", dop[state.direction[d]], d < state.direction.size() - 1 ? ' ' : '\n');
  printf("%dx%d (start: %d, %d) | Energy: %.0lf\n", n, m, si, sj, stateEnergy(state, false));
  for (int d = 0; d < n; d ++)
    printf("%s\n", table[d]);
  printf("------------------------------\n");
}

State bfs()
{
  State bestState; bestState.energy = 1e7;
  State base; base.insert({0, 0}, hp[0]);
  queue<State> q; q.push(base);
  while (!q.empty())
  {
    State u = q.front(); q.pop();
    // printState(u);
    if (u.direction.size() == hpSize - 1)
    {
      if (u.energy < bestState.energy) bestState = u;
      continue;
    }

    for (int k = 0; k < 4; k ++)
    {
      char nextProtein = hp[u.direction.size() + 1];
      int ii = u.i + dy[k], jj = u.j + dx[k];
      if (!u.has({ii, jj}))
      {
        State next = u; next.direction.push_back(k);
        next.insert({ii, jj}, nextProtein);
        if (nextProtein == 'H') if (nextProtein == 'H') for (int kk = 0, prevK = (k + 2) % 4; kk < 4; kk ++) if (prevK != kk) next.energy -= next.hVisited.count({ii + dy[kk], jj + dx[kk]});
        q.push(next);
      }
    }
  }
  return(bestState);
}

State Astar()
{
  int breakCount = 1000;
  State bestState; bestState.energy = 1e7;
  State base; base.insert({0, 0}, hp[0]);
  priority_queue<State> q; q.push(base);
  while (!q.empty())
  {
    State u = q.top(); q.pop();
    // printState(u);
    if (u.direction.size() == hpSize - 1) // Reached the end
    {
      if (u.energy < bestState.energy) bestState = u;
      else if (u.energy > bestState.energy) breakCount --;
      if (breakCount == 0) break;
      continue;
    }

    for (int k = 0; k < 4; k ++) // Adds each possible direction
    {
      char nextProtein = hp[u.direction.size() + 1];
      int ii = u.i + dy[k], jj = u.j + dx[k];
      if (!u.has({ii, jj}))
      {
        State next = u; next.direction.push_back(k);
        next.insert({ii, jj}, nextProtein);
        if (nextProtein == 'H') for (int kk = 0, prevK = (k + 2) % 4; kk < 4; kk ++) if (prevK != kk) next.energy -= next.hVisited.count({ii + dy[kk], jj + dx[kk]});
        next.value = u.value*0 + next.energy / (4*accumulatedEnergy[next.direction.size()]); // Heuristic value
        q.push(next);
      }
    }
  }
  return(bestState);
}

int main()
{
  while (scanf("%s", hp) != EOF)
  {
    getchar();
    baseEnergy = 0;
    hpSize = strlen(hp);
    accumulatedEnergy[0] = 1;
    for (int i = 0; i < hpSize - 1; i ++)
    {
      baseEnergy += (hp[i] == 'H') && (hp[i + 1] == 'H');
      accumulatedEnergy[i + 1] = baseEnergy + 1;
    }
    accumulatedEnergy[hpSize] = accumulatedEnergy[hpSize - 1];
    printf("Sequence of size %d: %s\n", hpSize, hp);

    // State best = bfs();
    State best = Astar();
    printf("Best energy: %.0lf\n", stateEnergy(best, true));
    printState(best);
    fflush(stdout);
  }

  return(0);
}

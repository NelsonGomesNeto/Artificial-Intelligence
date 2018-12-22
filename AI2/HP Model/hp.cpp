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
  State bestState; bestState.value = 1e7;
  State base; if (hp[0] == 'P') base.pVisited.insert({0, 0}); else base.hVisited.insert({0, 0});
  queue<State> q; q.push(base);
  while (!q.empty())
  {
    State u = q.front(); q.pop();
    // printState(u);
    if (u.direction.size() == hpSize - 1)
    {
      double energy = stateEnergy(u, true); u.value = energy;
      if (u.value < bestState.value) bestState = u;
      continue;
    }
    for (int k = 0; k < 4; k ++)
    {
      char nextProtein = hp[u.direction.size() + 1];
      int ii = u.i + dy[k], jj = u.j + dx[k];
      if ((nextProtein == 'P' && !u.pVisited.count({ii, jj})) || (nextProtein == 'H' && !u.hVisited.count({ii, jj})))
      {
        State next = u; next.direction.push_back(k);
        next.i = ii, next.j = jj;
        if (nextProtein == 'P') next.pVisited.insert({ii, jj});
        else
        {
          next.hVisited.insert({ii, jj});
          next.value = u.value + (hp[u.direction.size()] == 'H');
          for (int kk = 0; kk < 4; kk ++) next.value -= next.hVisited.count({ii + dy[kk], jj + dx[kk]});
        }
        // next.visited.insert({next.i, next.j}), next.value = -u.value*0.05 + ((accumulatedEnergy[next.direction.size() + 1] - 1)*1 + (stateEnergy(next, true) - baseEnergy)) / (accumulatedEnergy[next.direction.size() + 1]);
        printf("%lf\n", next.value);
        //-u.value*0 + stateEnergy(next, true) + accumulatedEnergy[next.direction.size() + 1] * 1;// accumulatedEnergy[next.direction.size()];
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
  State base; if (hp[0] == 'P') base.pVisited.insert({0, 0}); else base.hVisited.insert({0, 0});
  priority_queue<State> q; q.push(base);
  while (!q.empty())
  {
    State u = q.top(); q.pop();
    // printState(u);
    if (u.direction.size() == hpSize - 1)
    {
      if (u.energy <= bestState.energy) bestState = u;
      else breakCount --;
      if (breakCount == 0) break;
      continue;
    }
    for (int k = 0; k < 4; k ++)
    {
      char nextProtein = hp[u.direction.size() + 1];
      int ii = u.i + dy[k], jj = u.j + dx[k];
      if (!u.pVisited.count({ii, jj}) && !u.hVisited.count({ii, jj}))
      {
        State next = u; next.direction.push_back(k);
        next.i = ii, next.j = jj;
        if (nextProtein == 'P') next.pVisited.insert({ii, jj});
        else
        {
          next.hVisited.insert({ii, jj});
          next.energy = u.energy; // + (hp[u.direction.size()] == 'H');
          for (int kk = 0, prevK = (k + 2) % 4; kk < 4; kk ++) if (prevK != kk) next.energy -= next.hVisited.count({ii + dy[kk], jj + dx[kk]});
          next.value = u.value*0 + next.energy / (4*accumulatedEnergy[next.direction.size()]);
        }
        // next.visited.insert({next.i, next.j}), next.value = -u.value*0.05 + ((accumulatedEnergy[next.direction.size() + 1] - 1)*1 + (stateEnergy(next, true) - baseEnergy)) / (accumulatedEnergy[next.direction.size() + 1]);
        // printf("%lf\n", next.value);
        //-u.value*0 + stateEnergy(next, true) + accumulatedEnergy[next.direction.size() + 1] * 1;// accumulatedEnergy[next.direction.size()];
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
    fflush(stdout);
    // printState(best);
  }

  return(0);
}

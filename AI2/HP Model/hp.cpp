#include <bits/stdc++.h>
using namespace std;

int hpSize; char hp[(int) 1e6]; double baseEnergy = 0;
int dx[4] = {0, 0, 1, -1}, dy[4] = {1, -1, 0, 0}, n, m, si, sj;
char dop[4 + 1] = {'v', '^', '>', '<'}, table[1000][1000];

struct State
{
  vector<char> direction;
  int i = 0, j = 0;
  set<pair<int, int>> visited;
  double value;
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
  queue<State> q; q.push(State({}));
  q.front().visited.insert({0, 0});
  while (!q.empty())
  {
    State u = q.front(); q.pop();
    printState(u);
    if (u.direction.size() == hpSize - 1)
    {
      if (stateEnergy(u, false) < bestState.value) bestState = u;
      continue;
    }
    for (int k = 0; k < 4; k ++)
    {
      if (!u.visited.count({u.i + dy[k], u.j + dx[k]}))
      {
        State next = u; next.direction.push_back(k);
        next.i = u.i + dy[k], next.j = u.j + dx[k];
        next.visited.insert({next.i, next.j});
        q.push(State({next}));
      }
    }
  }
  return(bestState);
}

int main()
{
  scanf("%s", hp); hpSize = strlen(hp); for (int i = 0; i < hpSize - 1; i ++) baseEnergy += (hp[i] == 'H') && (hp[i + 1] == 'H');
  printf("Sequence of size %d: %s\n", hpSize, hp);

  State best = bfs();
  printf("Ended BFS:\n");
  printState(best);

  return(0);
}
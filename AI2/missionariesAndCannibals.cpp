#include <bits/stdc++.h>
#define DEBUG if(0)
using namespace std;
struct State
{
  int missionaries, cannibals; bool boat; int step; double value;
  bool operator<(const State &b) const { return(value < b.value || (value == b.value && step < b.step)); }
  bool operator>(const State &b) const { return(value > b.value || (value == b.value && step > b.step)); }
};
// true means that the boat the in the starting river
int missionaries = 3, cannibals = 3, allowedInBoat = 2;
int visited[1001][1001][2];
State stateParent[1001][1001][2];

void printSolution()
{
  for (int m = 0, c = 0, b = 0; m != missionaries || c != cannibals || !b;)
  {
    printf("[%d %d] river [%d %d] || boat: %s\n", m, c, missionaries - m, cannibals - c, b ? "left" : "right");
    int am = m, ac = c, ab = b;
    m = stateParent[am][ac][ab].missionaries, c = stateParent[am][ac][ab].cannibals, b = stateParent[am][ac][ab].boat;
  }
}

bool validState(int m, int c)
{
  return(!((m > 0 && c > m) || ((missionaries - m) > 0 && (cannibals - c) > (missionaries - m))));
}

int BFS()
{
  memset(visited, -1, sizeof(visited));
  queue<State> q; q.push({missionaries, cannibals, true, 0});
  while (!q.empty())
  {
    State s = q.front(); q.pop();
    DEBUG printf("[%d %d] [%d %d]\n", s.missionaries, s.cannibals, missionaries - s.missionaries, cannibals - s.cannibals);
    visited[s.missionaries][s.cannibals][s.boat] = s.step;
    if (!s.missionaries && !s.cannibals && !s.boat) break;
    if (s.boat)
    {
      // for (int m = min(s.missionaries, allowedInBoat); m >= 0; m --)
        // for (int c = min(s.cannibals, allowedInBoat); c >= 0; c --)
      for (int m = 0; m <= min(s.missionaries, allowedInBoat); m ++)
        for (int c = min(s.cannibals, allowedInBoat); c >= 0; c --)
          if (m + c > 0 && m + c <= allowedInBoat && validState(s.missionaries, s.cannibals) && visited[s.missionaries - m][s.cannibals - c][!s.boat] == -1)
            q.push({s.missionaries - m, s.cannibals - c, !s.boat, s.step + 1}), stateParent[s.missionaries - m][s.cannibals - c][!s.boat] = s;
    }
    else
    { // The boat cannot cross the river by itself
      for (int m = 0; m <= min(missionaries - s.missionaries, allowedInBoat); m ++)
        for (int c = 0; c <= min(cannibals - s.cannibals, allowedInBoat); c ++)
          if (m + c > 0 && m + c <= allowedInBoat && validState(missionaries - s.missionaries, cannibals - s.cannibals) && visited[s.missionaries + m][s.cannibals + c][!s.boat] == -1)
            q.push({s.missionaries + m, s.cannibals + c, !s.boat, s.step + 1}), stateParent[s.missionaries + m][s.cannibals + c][!s.boat] = s;
    }
  }
  return(visited[0][0][0]);
}

double heuristic(State &state)
{
  return(-(state.missionaries + state.cannibals + state.boat));
}

int Astar(double (*heuristic)(State&))
{
  memset(visited, -1, sizeof(visited));
  priority_queue<State> pq; pq.push({missionaries, cannibals, true, 0, 0});
  while (!pq.empty())
  {
    State s = pq.top(); pq.pop();
    // printf("%.3g\n", s.value);
    DEBUG printf("[%d %d] [%d %d]\n", s.missionaries, s.cannibals, missionaries - s.missionaries, cannibals - s.cannibals);
    visited[s.missionaries][s.cannibals][s.boat] = s.step;
    if (!s.missionaries && !s.cannibals && !s.boat) break;
    if (s.boat)
    {
      for (int m = 0; m <= min(s.missionaries, allowedInBoat); m ++)
        for (int c = 0; c <= min(s.cannibals, allowedInBoat); c ++)
          if (m + c > 0 && m + c <= allowedInBoat && validState(s.missionaries - m, s.cannibals - c) && visited[s.missionaries - m][s.cannibals - c][!s.boat] == -1)
          {
            State newState = {s.missionaries - m, s.cannibals - c, !s.boat, s.step + 1}; newState.value = heuristic(newState);
            pq.push(newState), stateParent[s.missionaries - m][s.cannibals - c][!s.boat] = s;
          }
    }
    else
    { // The boat cannot cross the river by itself
      for (int m = 0; m <= min(missionaries - s.missionaries, allowedInBoat); m ++)
        for (int c = 0; c <= min(cannibals - s.cannibals, allowedInBoat); c ++)
          if (m + c > 0 && m + c <= allowedInBoat && validState(s.missionaries + m, s.cannibals + c) && visited[s.missionaries + m][s.cannibals + c][!s.boat] == -1)
          {
            State newState = {s.missionaries + m, s.cannibals + c, !s.boat, s.step + 1}; newState.value = heuristic(newState);
            pq.push(newState), stateParent[s.missionaries + m][s.cannibals + c][!s.boat] = s;
          }
    }
  }
  return(visited[0][0][0]);
}

int main()
{
  while (scanf("%d %d %d", &missionaries, &cannibals, &allowedInBoat) != EOF)
  {
    int ans = Astar(heuristic);
    // int ans = BFS();
    if (ans != -1)
    {
      int states = 0; for (int i = 0; i < missionaries; i ++) for (int j = 0; j < cannibals; j ++) for (int k = 0; k < 2; k ++) states += visited[i][j][k] != -1;
      printf("%d missionaries, %d cannibals and %d-sized boat can cross the river in %d steps (visited %d states)\n", missionaries, cannibals, allowedInBoat, ans, states);
      // printSolution();
    }
    else printf("%d missionaries, %d cannibals and %d-sized boat can't cross the river\n", missionaries, cannibals, allowedInBoat);
  }
  return(0);
}
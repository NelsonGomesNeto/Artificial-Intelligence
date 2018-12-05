#include <bits/stdc++.h>
using namespace std;
const double inf = 1e18;
struct Movement { int i, j; double value; };
int n = 3, m = 3, winLineSize = 3;
char board[1000][1001], aux[1000][1001];

void resetBoard() { for (int i = 0; i < n; i ++) for (int j = 0; j < m; j ++) board[i][j] = ' '; }
int countNeighbours(int i, int j, int di, int dj)
{
  int neighbours = 0; char start = aux[i][j];
  while (i < n && j < m && aux[i][j] == start)
  {
    neighbours ++;
    aux[i][j] = ' ';
    i += di, j += dj;
  }
  return(neighbours);
}
double evaluateBoard()
{
  double value = 0;
  memcpy(aux, board, sizeof(board));
  for (int i = 0; i < n; i ++)
    for (int j = 0; j < m; j ++)
      if (board[i][j] != ' ')
      {
        value += (board[i][j] == 'O' ? 1.25 : -1.0) * countNeighbours(i, j, 0, 1);
        value += (board[i][j] == 'O' ? 1.25 : -1.0) * countNeighbours(i, j, 1, 0);
        value += (board[i][j] == 'O' ? 1.25 : -1.0) * countNeighbours(i, j, 1, 1);
      }
  return(value);
}

// It will alternate between minimum and maximum
// If (depth & 1): minimum; else maximum
// Therefore we'll need to evaluate a leaf somehow
// Let's first try with an even value, so that maximum will be the last
Movement miniMax(int depth)
{
  if (!depth) return(Movement({-1, -1, evaluateBoard()}));
  Movement bestMovement = {-1, -1, ((depth & 1) ? inf : -inf)};
  for (int i = 0; i < n; i ++)
    for (int j = 0; j < m; j ++)
      if (board[i][j] == ' ') // player can put a piece
      {
        board[i][j] = (depth & 1) ? 'O' : 'X';
        Movement m = miniMax(depth - 1);
        if (((depth & 1) && m.value < bestMovement.value)
        || (!(depth & 1) && m.value > bestMovement.value))
        {
          bestMovement = m;
          bestMovement.i = i, bestMovement.j = j;
        }
        board[i][j] = ' ';
      }
  return(bestMovement);
}

int main()
{
  resetBoard();
  Movement first = miniMax(4);
  printf("%d %d %.3g\n", first.i, first.j, first.value);
  return(0);
}
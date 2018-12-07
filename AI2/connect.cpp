#include <bits/stdc++.h>
using namespace std;
const double inf = 1e18;
struct Movement { int i, j; double value; };
int n = 5, m = 5, winLineSize = 4;
char board[1000][1001], aux[1000][1001];

void printBoard()
{
  for (int i = 0; i < n; i ++) printf("%s\n", board[i]);
}
void resetBoard() { for (int i = 0; i < n; i ++) for (int j = 0; j < m; j ++) board[i][j] = ' '; }
int countNeighbours(int i, int j, int di, int dj)
{
  int neighbours = 0; char start = aux[i][j];
  while (i < n && j < m && aux[i][j] == start)
  {
    neighbours ++;
    i += di, j += dj;
  }
  return(neighbours);
}
double evaluateBoard(char wanted)
{
  double value = 0;
  memcpy(aux, board, sizeof(board));
  for (int i = 0; i < n; i ++)
    for (int j = 0; j < m; j ++)
      if (board[i][j] != ' ')
      {
        value += (board[i][j] == wanted ? 1.25 : 0.5) * pow(countNeighbours(i, j, 0, 1), 4); // 4 is the best
        value += (board[i][j] == wanted ? 1.25 : 0.5) * pow(countNeighbours(i, j, 1, 0), 4);
        value += (board[i][j] == wanted ? 1.25 : 0.5) * pow(countNeighbours(i, j, 1, 1), 4);
      }
  return(value);
}
int winner()
{
  memcpy(aux, board, sizeof(board));
  for (int i = 0; i < n; i ++)
    for (int j = 0; j < m; j ++)
      if (board[i][j] != ' ')
        if (countNeighbours(i, j, 0, 1) == winLineSize || countNeighbours(i, j, 1, 0) == winLineSize || countNeighbours(i, j, 1, 1) == winLineSize)
          return(board[i][j] == 'O' ? 1 : 2);
  return(0);
}

// It will alternate between minimum and maximum
// If (depth & 1): minimum; else maximum
// Therefore we'll need to evaluate a leaf somehow
// Let's first try with an even value, so that maximum will be the last
Movement miniMax(int depth, char player)
{
  if (!depth) return(Movement({-1, -1, evaluateBoard(player)}));
  Movement bestMovement = {-1, -1, ((depth & 1) ? inf : -inf)};
  for (int i = 0; i < n; i ++)
    for (int j = 0; j < m; j ++)
      if (board[i][j] == ' ') // player can put a piece
      {
        board[i][j] = (depth & 1) ? 'O' : 'X';
        Movement m = miniMax(depth - 1, player == 'O' ? 'X' : 'O');
        if (((depth & 1) && m.value < bestMovement.value)
        || (!(depth & 1) && m.value > bestMovement.value))
        {
          bestMovement = m;
          bestMovement.i = i, bestMovement.j = j;
        }
        board[i][j] = ' ';
      }
  if (bestMovement.value == ((depth & 1) ? inf : -inf)) bestMovement.value = evaluateBoard(player);
  return(bestMovement);
}

void play()
{
  int available = n * m; char player = 'O';
  printBoard();
  while (available -- && !winner())
  {
    Movement mov = miniMax(player == 'O' ? 9 : 8, player);
    if (mov.i == -1 && mov.j == -1) printf("Something very wrong is happening\n");
    board[mov.i][mov.j] = player;
    printf("Player %c at %d %d\n", player, mov.i, mov.j);
    printBoard();
    player = player == 'O' ? 'X' : 'O';
  }
  int won = winner();
  if (!won) printf("Tie!\n");
  else printf("Player %c won\n", won == 1 ? 'O' : 'X');
}

int main()
{
  resetBoard();
  play();
  return(0);
}

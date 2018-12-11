#include <bits/stdc++.h>
using namespace std;
struct State
{
  int missionaries, cannibals; bool boat; int step; double value;
  bool operator<(const State &b) const { return(value < b.value || (value == b.value && step < b.step)); }
  bool operator>(const State &b) const { return(value > b.value || (value == b.value && step > b.step)); }
};
int missionaries = 3, cannibals = 3, allowedInBoat = 2;
set<Being> lol;
vector<State> chromosome;

/* Strategy:
Chromosome: List of genes (nodes) instead of a vector
Crossing: False :)
Mutation: Generate new genes based on available movements
Adaption: state.missionaries + state.cannibals + state.boat
*/

int main()
{
  return(0);
}

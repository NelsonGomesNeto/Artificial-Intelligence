class Position {
  constructor(i, j) {
    this.i = i;
    this.j = j;
  }
  equal(a) {
    return(this.i == a.i && this.j == a.j);
  }
}
let di = [-1, 0, 0, 1], dj = [0, -1, 1, 0];

class PathFinder {
  constructor(origin, destination) {
    this.origin = new Position(int(origin.y / lineSize), int(origin.x / columnSize));
    this.destination = new Position(int(destination.y / lineSize), int(destination.x / columnSize));
    this.visited = new Array(lines);
    for (let i = 0; i < lines; i ++) {
      this.visited[i] = new Array(columns);
      for (let j = 0; j < columns; j ++)
        this.visited[i][j] = false;
    }
  }

  invalid(i, j) {
    return(i < 0 || j < 0 || i >= lines || j >= columns || this.visited[i][j] || gameMap.matrix[i][j]);
  }

  findPath() {
    var queue = new Queue();
    queue.push([this.origin, []]);
    while (!queue.empty()) {
      var u = queue.pop();
      if (u[0].equal(this.destination)) return(u[1]);
      if (this.invalid(u[0].i, u[0].j)) continue;
      this.visited[u[0].i][u[0].j] = true;
      for (var k = 0; k < 4; k ++) {
        let next = new Position(u[0].i + di[k], u[0].j + dj[k]);
        let nextPath = [...u[1]];
        nextPath.push(next);
        queue.push([next, nextPath]);
      }
    }
    return(false);
  }
}
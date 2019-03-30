class GameMap {
  constructor() {
    this.matrix = new Array(lines);
    this.peopleInMatrix = new Array(lines);
    this.teamInMatrix = new Array(lines);
    for (var i = 0; i < lines; i ++) {
      this.matrix[i] = new Array(columns);
      this.peopleInMatrix[i] = new Array(columns);
      this.teamInMatrix[i] = new Array(columns);
      for (var j = 0; j < columns; j ++) {
        this.matrix[i][j] = false;
        this.peopleInMatrix[i][j] = 0;
        this.teamInMatrix[i][j] = 0;
      }
    }

    for (var j = 0; j < columns; j ++)
      if (j % 10 == 0){
        var a = true;
        for (var i = 0; i < lines; i ++){
          if ((i + j / 10) % 10 == 0) a = !a;
          if (a) this.matrix[i][j] = true;
        }
      }
  }

  display() {
    for (var i = 0; i < lines; i ++) {
      for (var j = 0; j < columns; j ++) {
        if (this.matrix[i][j])
          rect(j * columnSize, i * lineSize, columnSize, lineSize);
      }
    }
  }
}
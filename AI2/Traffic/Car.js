class Car {
  constructor(id, position, destination, col) {
    this.id = id;
    this.position = position;
    hasCar[this.position.y][this.position.x] = true;
    this.destination = destination;
    this.col = col;
    this.chosen = -1;
    this.reachedDestination = false;
  }

  display() {
    stroke(0, 0, 0);
    fill(this.col);
    push();
      translate((this.position.x + 0.25) * xScale, (this.position.y + 0.25) * yScale);
      rect(0, 0, 0.5 * xScale, 0.5 * yScale);
      fill(0, 0, 0);
      text(this.id.toString(), 0.15 * xScale, 0.35 * yScale);
    pop();
  }

  update() {
    if (this.position.x == this.destination.x && this.position.y == this.destination.y) {
      if (!this.reachedDestination) {
        logStrings.push("carro " + this.id.toString() + " chegou no destino");
        hasCar[this.position.y][this.position.x] = false;
      }
      this.reachedDestination = true;
      return;
    }
    if (this.chosen == -1) {
      var allowedDirections = [];
      for (var i = 0; i < 4; i ++)
        if (roadsDirections[this.position.y][this.position.x][i])
          allowedDirections.push(i);
      this.chosen = allowedDirections[int(random(0, allowedDirections.length))];
    }
    let nextPosition = createVector(this.position.x + dj[this.chosen], this.position.y + di[this.chosen]);
    if (hasCar[nextPosition.y][nextPosition.x] && random(0, 5) > 4) {
      logStrings.push("carro " + this.id.toString() + " teve que esperar");
      return;
    }
    hasCar[this.position.y][this.position.x] = false;
    this.position = nextPosition.copy();
    hasCar[this.position.y][this.position.x] = true;
    this.chosen = -1;
  }
}
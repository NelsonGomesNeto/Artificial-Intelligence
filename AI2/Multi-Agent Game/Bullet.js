class Bullet {
  constructor(startPosition, angle) {
    this.position = startPosition;
    this.velocity = createVector(5, 0);
    this.angle = angle;
    this.velocity.rotate(this.angle);
    this.isOffScreen = false;
  }

  update() {
    this.position.add(this.velocity);
    if (this.position.x < 0 || this.position.x > width || this.position.y < 0 || this.position.y > height) {
      this.isOffScreen = true;
    }
  }

  display() {
    push();
      translate(this.position.x, this.position.y);
      rotate(this.angle);
      fill(255, 0, 0);
      rect(0, 0, 10, 5);
    pop();
  }
}
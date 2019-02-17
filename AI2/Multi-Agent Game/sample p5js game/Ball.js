class Ball {
  constructor() {
    this.position = createVector(width / 2, height / 2);
    this.radious = random(1, 10);
    this.velocity = createVector(random(-2, 2), random(-2, 2));
    this.acceleration = createVector(0, 0.01*gravityConstant);
    this.topSpeed = 10;
  }

  update() {
    this.velocity.add(this.acceleration);
    this.velocity.limit(this.topSpeed);
    this.position.add(this.velocity);
    this.checkEdges();
  }

  checkEdges() {
    if (this.position.x + this.radious > width || this.position.x - this.radious < 0)
      this.velocity.x *= -1;
    if (this.position.y + this.radious > height || this.position.y - this.radious < 0)
      this.velocity.y *= -1;
  }

  display() {
    fill(0, 0, 0);
    ellipse(this.position.x, this.position.y, this.radious, this.radious);
  }
}
class Spaceship {
  constructor() {
    this.position = new createVector(width / 2, height / 2);
    this.velocity = new createVector(0, 0);
    this.acceleration = new createVector(0, 0);
    this.angle = 0;
    this.aVelocity = 0;
    this.aAcceleration = 0;
    this.topSpeed = 10;
  }

  move() {
    if (keyIsDown(UP_ARROW)) {
      spaceship.acceleration.set(0, -0.1);
      spaceship.acceleration.rotate(spaceship.angle);
    }
    if (keyIsDown(DOWN_ARROW)) {
      spaceship.acceleration.set(0, 0.1);
      spaceship.acceleration.rotate(spaceship.angle);
    }
    if (keyIsDown(LEFT_ARROW))
      spaceship.angle += -pi/20;
    if (keyIsDown(RIGHT_ARROW))
      spaceship.angle += pi/20;
    if (!keyIsPressed) {
      spaceship.acceleration.set(0, 0);
    }
  }

  update() {
    this.velocity.add(this.acceleration);
    this.velocity.limit(this.topSpeed);
    this.position.add(this.velocity);
    this.aVelocity += this.aAcceleration;
    this.aVelocity = constrain(this.aVelocity, -0.3, 0.3);
    this.angle += this.aVelocity;
    //this.acceleration.mult(0);
  }

  checkEdges() {
    if (this.position.x > width) {
      this.position.x = 0;
    } else if (this.position.x < 0) {
      this.position.x = width;
    }
    if (this.position.y > height) {
      this.position.y = 0;
    } else if (this.position.y < 0) {
      this.position.y = height;
    }
  }

  display() {
    push();
      translate(this.position.x, this.position.y);
      rotate(this.angle);
      fill(255, 30, 0);
      rect(-8, 1, 2, 3); rect(7, 1, -2, 3);
      fill(17, 0, 255);
      triangle(-10, 1, 10, 1, 0, -20);
    pop();
  }
}
class Person {
  constructor() {
    this.position = createVector(width / 2, height / 2);
    this.velocity = createVector(0, 0);
    this.acceleration = createVector(0, 0);
    this.angle = 0;
    this.topSpeed = 2;
    this.color = color(0, 0, 255);
    this.size = 20;
    this.bullets = new Array();
  }

  shot(angle) {
    this.bullets.push(new Bullet(this.position.copy(), angle));
  }

  getMovements() {
    this.angle = atan2(mouseY - this.position.y, mouseX - this.position.x);
    if (mouseIsPressed) {
      if (mouseButton === LEFT) this.shot(this.angle);
    }
    if (keyIsPressed) {
      this.acceleration.set((true===keyIsDown(RIGHT_ARROW)) - (true===keyIsDown(LEFT_ARROW)),
                            (true===keyIsDown(DOWN_ARROW)) - (true===keyIsDown(UP_ARROW)));
      this.acceleration.rotate(this.angle + Math.PI / 2);
    } else {
      this.velocity.mult(0), this.acceleration.mult(0);
    }
  }

  checkEdges() {
    if (this.position.x > width || this.position.x < 0)
      this.velocity.x = this.acceleration.x = 0;
    if (this.position.y > height || this.position.y < 0)
      this.velocity.y = this.acceleration.y = 0;
  }

  update() {
    this.getMovements();
    for (var i = 0; i < this.bullets.length; i ++)
      this.bullets[i].update();
    this.velocity.add(this.acceleration);
    this.velocity.limit(this.topSpeed);
    this.position.add(this.velocity);
    this.checkEdges();
  }

  display() {
    push();
      translate(this.position.x, this.position.y);
      rotate(this.angle);
      fill(this.color);
      ellipse(0, 0, this.size, this.size);
      triangle(0, 0 - 2*this.size,
               0 + 2*this.size, 0,
               0, 0 + 2*this.size);
    pop();
    for (var i = 0; i < this.bullets.length; i ++) {
      this.bullets[i].display();
      if (this.bullets[i].isOffScreen) this.bullets.splice(i --, 1);
    }
    fill(255, 255, 255);
    text(this.bullets.length, 0, height - 10);
  }
}
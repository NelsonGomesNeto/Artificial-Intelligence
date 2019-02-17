class Person {
  constructor() {
    this.position = createVector(random(width / 5, 4 * width / 5), random(height / 5, 4 * height / 5));
    this.velocity = createVector(0, 0);
    this.acceleration = createVector(0, 0);
    this.angle = 0;
    this.topSpeed = 2;
    this.color = color(random(0, 255), random(0, 255), random(0, 255));
    this.size = 20;
    this.activated = false;
    this.id = idCounter ++;
    this.health = maxHealth;
    this.bullets = new Array();
  }

  shot(angle) {
    this.bullets.push(new Bullet(this.position.copy(), angle, this.id));
  }

  getMovements() {
    if (this.activated) this.angle = atan2(mouseY - this.position.y, mouseX - this.position.x);
    if (mouseIsPressed) {
      if (this.activated && mouseButton === LEFT) this.shot(this.angle);
      if (mouseButton === CENTER &&
          this.position.x - this.size*1.1 <= mouseX && mouseX <= this.position.x + this.size*1.1 &&
          this.position.y - this.size*1.1 <= mouseY && mouseY <= this.position.y + this.size*1.1)
        this.activated = !this.activated, mouseButton = -1;
    }
    if (this.activated && keyIsPressed) {
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
      triangle(0, 0 - this.size,
               0 + this.size, 0,
               0, 0 + this.size);
      fill(0, 255, 0);
      rect(-this.size, -20, 10, 40);
      fill(255, 0, 0);
      let healthPorcentage = (maxHealth - this.health) / maxHealth;
      rect(-this.size, 40 / 2 - (40 * healthPorcentage), 10, 40 * healthPorcentage);
    pop();
    for (var i = 0; i < this.bullets.length; i ++) {
      this.bullets[i].display();
      if (this.bullets[i].isOffScreen) this.bullets.splice(i --, 1);
    }
    fill(255, 255, 255);
    text(this.bullets.length, 0, height - 10);
  }
}
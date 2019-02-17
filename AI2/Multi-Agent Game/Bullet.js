class Bullet {
  constructor(startPosition, angle, id) {
    this.position = startPosition;
    this.velocity = createVector(5, 0);
    this.angle = angle;
    this.velocity.rotate(this.angle);
    this.isOffScreen = false;
    this.id = id;
  }

  update() {
    this.position.add(this.velocity);
    if (this.position.x < 0 || this.position.x > width || this.position.y < 0 || this.position.y > height) {
      this.isOffScreen = true;
    }
    if (!this.isOffScreen)
      for (var i = 0; i < people.length; i ++)
        if (people[i].id != this.id
        && people[i].position.x - people[i].size <= this.position.x && this.position.x <= people[i].position.x + people[i].size
        && people[i].position.y - people[i].size <= this.position.y && this.position.y <= people[i].position.y + people[i].size)
          people[i].health -= 5, this.isOffScreen = true;
  }

  display() {
    push();
      translate(this.position.x, this.position.y);
      rotate(this.angle);
      fill(255, 0, 0);
      rect(0, -2.5, 10, 5);
    pop();
  }
}
class Person {
  constructor(teamID) {
    if (teamID === 1)
      this.position = createVector(random(0, spawnSize), random(0, height));
      //this.position = createVector(random(width / 6, 5 * width / 6), random(height / 8, 7 * height / 8));
    else
      this.position = createVector(random(width - spawnSize, width), random(0, height));
    this.velocity = createVector(0, 0);
    this.acceleration = createVector(0, 0);
    this.angle = 0;
    this.topSpeed = 2;
    this.size = personSize;
    this.activated = false;
    this.id = idCounter ++;
    this.teamID = teamID;
    this.bullets = [];
    this.healings = [];
    this.fireCounter = -1;
    this.fieldOfViewCounter = -1;
    this.pathID = 1;
    this.path = false;
    this.target = new Position(-1, -1);
    this.enemiesAhead = new Array();
    /* Extended classes must define:
      color, damage, health, fullHealth, cooldown, bulletWillHit (function)
    */
  }

  static bulletWillHit(personID, bulletID) {
    return(personID !== bulletID);
  }

  shot() {
    this.bullets.push(new Bullet(this.position.copy(), this.angle, this.id, this.teamID, this.damage, Person.bulletWillHit));
  }

  getMovements() {
    if (this.activated) this.angle = atan2(mouseY - this.position.y, mouseX - this.position.x);
    
    if (mouseIsPressed) {
      if (this.activated && mouseButton === LEFT && this.fireCounter === 0){
        this.shot();
        this.fireCounter ++;
      }

      if (mouseButton === CENTER &&
          this.position.x - this.size*1.1 <= mouseX && mouseX <= this.position.x + this.size*1.1 &&
          this.position.y - this.size*1.1 <= mouseY && mouseY <= this.position.y + this.size*1.1){
        this.activated = !this.activated, mouseButton = -1;
      }
    }
    if (this.activated && keyIsPressed) {
      this.acceleration.set((true===keyIsDown(aKey)) - (true===keyIsDown(dKey)),
                            (true===keyIsDown(sKey)) - (true===keyIsDown(wKey)));
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

  followPath() {
    let i = int(this.position.y / lineSize), j = int(this.position.x / columnSize);
    if (!this.path || this.pathID >= (this.path.length - 1)) {
      this.path = new PathFinder(this.position.copy(), createVector(random(0, width - 100), random(0, height - 100))).findPath();
      this.pathID = -1;
    } else if (this.pathID >= 0 && (i !== this.target.i || j !== this.target.j)) {
      this.velocity.set(this.topSpeed, 0);
      this.angle = atan2(this.target.i - i, this.target.j - j);
      this.velocity.rotate(this.angle);
    } else if (this.path && this.pathID < this.path.length - 1) {
      this.pathID ++;
      this.target.i = this.path[this.pathID].i, this.target.j = this.path[this.pathID].j;
    }
  }

  validPosition(position) {
    let i = min(int(position.y / lineSize), lines - 1), j = min(int(position.x / columnSize), columns - 1);
    return(position.x >= 0 && position.x < width && position.y >= 0 && position.y < height && !gameMap.matrix[i][j]);
  }

  lightBeam(direction) {
    var position = this.position.copy();
    while (this.validPosition(position)) {
      let i = min(int(position.y / lineSize), lines - 1), j = min(int(position.x / columnSize), columns - 1);
      if (gameMap.peopleInMatrix[i][j] && gameMap.peopleInMatrix[i][j] != this.id && gameMap.teamInMatrix[i][j] != this.teamID) {
        if (this.enemiesAhead.length >= 5) this.enemiesAhead.shift();
        this.enemiesAhead.push(position.copy());
      }
      position.add(direction);
    }
  }

  findEnemiesAhead() {
    for (var i = 1; i <= bulletsInFieldOfView; i ++) {
      let beam = createVector(10, 0);
      beam.rotate(this.angle - fieldOfViewAngle + 2*fieldOfViewAngle*(i/bulletsInFieldOfView));
      this.lightBeam(beam)
    }
  }

  atack() {
    if (this.enemiesAhead.length) {
      let chosen = int(random(0, this.enemiesAhead.length - 1));
      let prevAngle = this.angle;
      this.angle = atan2(this.enemiesAhead[chosen].y - this.position.y, this.enemiesAhead[chosen].x - this.position.x);
      if (this.fireCounter % this.cooldown == 0) this.shot();
      this.angle = prevAngle;
    }
  }

  update() {
    let i;
    if ((++ this.fireCounter) % this.cooldown == 0) this.fireCounter = 0;

    if ((++ this.fieldOfViewCounter) % fieldOfViewCooldown == 0) {
      this.findEnemiesAhead();
      this.fieldOfViewCounter = 0;
    }

    if (this.teamID === 1) this.getMovements();
    else {
      this.followPath();
      this.atack();
    }

    for (i = 0; i < this.bullets.length; i ++)
      this.bullets[i].update();
    for (i = 0; i < this.healings.length; i ++)
      this.healings[i].update(this.position);
    // for (i = 0; i < this.enemiesAhead.length; i ++)
    //   this.enemiesAhead.

    this.velocity.add(this.acceleration);
    this.velocity.limit(this.topSpeed);
    this.position.add(this.velocity);
    let y = min(int(this.position.y / lineSize), lines - 1), x = min(int(this.position.x / columnSize), columns - 1);
    if (gameMap.matrix[y][x]) this.position.sub(this.velocity);
    gameMap.peopleInMatrix[y][x] = this.id;
    gameMap.teamInMatrix[y][x] = this.teamID;
    this.checkEdges();
  }

  drawLifeBar() {
    push();
      translate(0, 10);
      rotate(-Math.PI / 2);
      fill(0, 255, 0);
      rect(-this.size, -this.size, this.size / 2, 2 * this.size);
      fill(255, 0, 0);
      let healthPorcentage = (this.fullHealth - this.health) / this.fullHealth;
      rect(-this.size, this.size - (2 * this.size * healthPorcentage), this.size / 2, 2 * this.size * healthPorcentage);
    pop();
  }

  drawFieldOfView() {
    fill(255, 0, 0, 50);
    arc(0, 0, max(width, height), max(width, height), -fieldOfViewAngle, fieldOfViewAngle, PIE);
  }

  display() {
    let i;
    push();
      translate(this.position.x, this.position.y);
      this.drawLifeBar();
      rotate(this.angle);
      this.drawFieldOfView();
      fill(this.color);
      ellipse(0, 0, this.size, this.size);
      triangle(0, 0 - this.size,
               0 + this.size, 0,
               0, 0 + this.size);
      fill(255, 255, 255); textSize(this.size);
      rotate(Math.PI / 2); text(this.teamID, -this.size / 3, 0);
    pop();

    for (i = 0; i < this.bullets.length; i++) {
      this.bullets[i].display();
      if (this.bullets[i].isOffScreen) 
        this.bullets.splice(i--, 1);
    }
  }
}
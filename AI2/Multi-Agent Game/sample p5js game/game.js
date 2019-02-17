let pi = Math.PI;
let gravityConstant = 9.8;
var spaceship;
var balls;

function setup() {
  createCanvas(600, 600);
  spaceship = new Spaceship();
  balls = new Array();
  for (var i = 0; i < 1000; i ++)
    balls.push(new Ball());
}

function draw() {
  background(255, 155, 255);
  spaceship.move();
  spaceship.update();
  spaceship.checkEdges();
  spaceship.display();

  for (var i = 0; i < balls.length; i ++) {
    balls[i].update();
    balls[i].display();
    // text(balls[i].velocity, 0, height - 20);
    // text(balls[i].position, 0, height - 30);
  }
}
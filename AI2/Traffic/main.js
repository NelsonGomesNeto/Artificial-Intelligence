let width = 800, height = 800;
let n = 19, m = 19; var hasRoad, hasCar, roadsDirections;
var xScale, yScale;
// right, up, left, down
let dj = [1, 0, -1, 0], di = [0, -1, 0, 1];
var cars;
var logStrings = [];

function setup() {
  angleMode(DEGREES);
  // frameRate(4);
  createCanvas(width, height);
  xScale = width / m, yScale = height / n;

  hasRoad = new Array(n), hasCar = new Array(n), roadsDirections = new Array(n);
  for (var i = 0; i < n; i ++) {
    hasRoad[i] = new Array(m), hasCar[i] = new Array(m), roadsDirections[i] = new Array(m);
    for (var j = 0; j < m; j ++)
      hasRoad[i][j] = hasCar[i][j] = false, roadsDirections[i][j] = [0, 0, 0, 0];
  }
  for (var i = 0; i < n; i ++) {
    hasRoad[i][0] = hasRoad[i][6] = hasRoad[i][12] = hasRoad[i][18] = true;
    if (i < n - 1) roadsDirections[i][0][3] = roadsDirections[i][6][3] = true;
    if (i > 0) roadsDirections[i][12][1] = roadsDirections[i][18][1] = true;
  }
  for (var j = 0; j < m; j ++) {
    hasRoad[0][j] = hasRoad[6][j] = hasRoad[12][j] = hasRoad[18][j] = true;
    if (j > 0) roadsDirections[0][j][2] = roadsDirections[12][j][2] = true;
    if (j < m - 1) roadsDirections[6][j][0] = roadsDirections[18][j][0] = true;
  }

  colorMode(HSB, 100);
  cars = new Array(20);
  for (var i = 0; i < 20; i ++) {
    var position = createVector(int(random(0, m - 1)), int(random(0, n - 1)));
    while (!hasRoad[position.y][position.x] || hasCar[position.y][position.x]) position = createVector(int(random(0, m - 1)), int(random(0, n - 1)));
    var destination = createVector(int(random(0, m)), int(random(0, n)));
    while (!hasRoad[destination.y][destination.x]) destination = createVector(int(random(0, m)), int(random(0, n)));
    cars[i] = new Car(i, position, destination, color((i / 20) * 100, 100, 100));
    logStrings.push("carro " + i.toString() + " iniciou na posição (" + position.y.toString() + ", " + position.x.toString() + ") "
                  + "tem como destino (" + destination.y.toString() + ", " + destination.x.toString() + ")");
  }
  colorMode(RGB, 255);
}

function drawArrow(i, j, k) {
  strokeWeight(2); stroke(0, 255, 0);
  push();
    translate((j + 0.5) * xScale, (i + 0.5) * yScale);
    rotate(-k*90);
    line(0.1 * yScale, 0, 0.3 * yScale, 0);
    line(0.3 * yScale, 0, 0.2 * yScale, 0.1 * xScale);
    line(0.3 * yScale, 0, 0.2 * yScale, -0.1 * xScale);
  pop();
}

function drawGrid() {
  for (var i = 0; i < n; i ++)
    for (var j = 0; j < m; j ++) {
      strokeWeight(1); stroke(0, 0, 0);
      if (hasRoad[i][j]) fill(0, 0, 255);
      else fill(255, 0, 0);
      rect(j * xScale, i * yScale, (j + 1) * xScale, (i + 1) * yScale);
      for (var k = 0; k < 4; k ++) if (roadsDirections[i][j][k]) drawArrow(i, j, k);
    }
}

function draw() {
  background(255, 255, 255);

  drawGrid();
  for (var i = 0; i < cars.length; i ++) {
    cars[i].update();
    cars[i].display();
  }
}

function keyReleased() {
  if (key == 'p') saveStrings(logStrings, "log.txt");
}
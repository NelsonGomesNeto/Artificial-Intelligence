var people;

function setup() {
  createCanvas(600, 600);
  people = new Array();
  people.push(new Person());
}

function draw() {
  background(0, 0, 0);

  for (var i = 0; i < people.length; i ++) {
    people[i].update();
    people[i].display();
  }
}
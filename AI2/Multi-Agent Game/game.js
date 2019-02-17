let maxHealth = 100;
var people;
var idCounter = 0;

function setup() {
  createCanvas(600, 600);
  people = new Array();
  for (var i = 0; i < 10; i ++) people.push(new Person());
}

function draw() {
  background(0, 0, 0);

  for (var i = 0; i < people.length; i ++) {
    if (people[i].health <= 0) {
      people.splice(i --, 1);
      continue;
    }
    people[i].update();
    people[i].display();
  }
}
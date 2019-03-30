class Healing {
  constructor(position, personID, teamID) {
    this.position = position;
    this.personID = personID;
    this.teamID = teamID;
    this.pulse = 1;
    this.direction = 1;
    this.counterPulse = 0;
    this.empty = false;
  }

  update(position) {

    this.position = position;
    this.pulse += this.direction;

    if (this.pulse > 25){
      this.direction = -1;
      this.counterPulse++;
    }
    if (this.pulse < 0){
      this.direction = 1;
      this.counterPulse++;
    }
    if (this.counterPulse > 10) 
      this.empty = true;

    if (!this.empty)
      for (let i = 0; i < people.length; i ++)
        if (people[i].id !== this.personID && people[i].teamID === this.teamID
            && people[i].position.x - people[i].size + 15 <= this.position.x 
            && this.position.x <= people[i].position.x + people[i].size + 15
            && people[i].position.y - people[i].size + 15 <= this.position.y 
            && this.position.y <= people[i].position.y + people[i].size + 15) {
          people[i].health += 0.06;
          people[i].health = min(people[i].health, people[i].fullHealth);
        }

  }

  display() {
    push();
      noStroke();
      circle(this.position.x, this.position.y, this.pulse);
    pop();
  }
}
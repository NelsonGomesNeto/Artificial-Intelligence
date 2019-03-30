class Shooter extends Person {
  constructor(teamID) {
    super(teamID);
    this.color = color(0, 0, 255);
    this.damage = 25;
    this.health = maxHealth;
    this.fullHealth = this.health;
    this.cooldown = 10;
  }
}
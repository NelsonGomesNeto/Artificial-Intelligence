class Queue {
  constructor() {
    this.data = [];
  }
  push(data) {
    this.data.push(data);
  }
  pop() {
    return(this.data.shift());
  }
  empty() {
    return(this.data.length == 0);
  }
}
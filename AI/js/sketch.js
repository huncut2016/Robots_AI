let map;

function setup() {
  createCanvas(800, 800);
  map = new Map(10);
}

function draw() {
  background(0);

  map.update();
  map.show();
}

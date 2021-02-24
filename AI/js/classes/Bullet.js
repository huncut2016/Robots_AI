class Bullet {
    constructor ({x, y, velocity, demage, direction, ID}) {
        this.demage = demage;
        this.ID = ID;
        this.vel = velocity;
        this.pos = createVector(x, y);
        this.direction = direction;
    }

    update () {
        let velocity = p5.Vector.fromAngle(this.direction, this.vel)
        this.pos.add(velocity);
    }

    show() {
        stroke(255);
        fill('rgba(0,255,0, 0.25)');
        ellipse(this.pos.x , this.pos.y, 10)
    }

}
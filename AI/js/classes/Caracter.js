class Caracter {
    constructor({ID, direction, x, y, velocity, demage, HP, capacity, reloadTime, bulletVelocity}){
        this.pos = createVector(x, y); 
        this.ID = ID;
        this.bulletVelocity = bulletVelocity;
        this.vel = velocity;
        this.demage = demage;
        this.capacity = capacity;
        this.HP = HP === undefined ? 100 : HP;
        this.rank;
        this.reloadTime = reloadTime;
        this.direction = direction;
        this.isShot = false;
        this.visible = true;
    }

    update (){
        let velocity = p5.Vector.fromAngle(this.direction, this.vel)
        this.pos.add(velocity);
        this.isShot = Math.random() < 0.005 ? true : false;
    }

    show () {
        fill(255);
        ellipse(this.pos.x , this.pos.y, 25)
    }

    dead (rank) {
        this.HP = 0;
        this.rank = rank;

    }

    shot () {
        if(this.isShot && this.visible && this.capacity){
            this.capacity --;
            return new Bullet({
                x: this.pos.x,
                y: this.pos.y,
                velocity: this.bulletVelocity,
                demage: this.demage,
                direction: this.direction,
                ID: this.ID
            });

        } 
    }
}